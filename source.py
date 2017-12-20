__author__ = "Harshini Bonam"

import main_table
import math

# Function to find whether the given active user list of items contain a NULL value.
def get_null_item(active_user, db):
    for item in db[active_user] :
        if (db[active_user][item] == ""):
            return item
    return 0

# Function to compute the list of similarity value for the items which are commonly rated by active users
def get_similarity(userj, userk, items, pref_rating, db):

    # Function to find the common items
    def get_common(userj, userk,items, db):
        common = []
        for item in items:
            uj_r = db[userj][item]
            uk_r = db[userk][item]
            if( (uj_r != "") & (uk_r != "")):
                common.append(item)
        return common

    # Function to find the root mean square between two user ratinngs
    def root_mean_square(uj_r, uk_r, pref_rating):
        rms = 0
        for i in range(5):
            rms = rms + ((pref_rating[uj_r][i] - pref_rating[uk_r][i])**2)
        rms = rms / 5
        rms = math.sqrt(rms)
        return round(rms,3)

    try :
        common_rated_items = get_common(userj,userk,items,db)
        n = len(common_rated_items)
        similarity = 0
        for i in range(n):
            uj_rating = db[userj][common_rated_items[i]]
            uk_rating = db[userk][common_rated_items[i]]
            similarity = similarity + (1 - (root_mean_square(uj_rating, uk_rating, pref_rating)))
        if similarity != None :
            similarity = (similarity)/n
            return round(similarity,3)
    except:
        pass

# Function to find the top3 users that have maximum similarity value
def get_top3_keys(similarities):
    sorted_similarity_values = get_top3_values(similarities)
    top3_keys = [user for user in similarities.keys() if similarities[user] in sorted_similarity_values[:3]]
    return top3_keys

# Function to find the top3 values of similarities
def get_top3_values(similarities):
    return sorted(similarities.values(), reverse= True)[:3]

# Function to compute the preference matrix from the top3 users
def get_pref_matrix(top3, pref_rating, null_item, db):
    p_matrix = []
    for i in range(3):
        p_matrix.append(pref_rating[db[top3[i]][null_item]])
    return p_matrix

# Function to compute the normalized similarities of the top3 users
def get_normalized_similarities(top3_similarities):
    sum_of_similarities = 0
    for i in top3_similarities:
        sum_of_similarities = sum_of_similarities + i
    return [round(val / sum_of_similarities, 3) for val in top3_similarities]

# Function to compute the predictive precedence value
def get_predictive_precedence(normalized_similarities, preference_matrix):

    # Function to multiply two matrices
    def matrix_multiply(normalized_similarities, preference_matrix):
        matrix_mul = [0,0,0,0,0]
        try:
            for i in range(5):
                matrix_mul[i] = 0
                for j in range(3):
                    matrix_mul[i] = matrix_mul[i] + (normalized_similarities[j] * preference_matrix[j][i])
            return matrix_mul
        except Exception as e:
            print e

    result = matrix_multiply(normalized_similarities, preference_matrix)
    sum_of_elements = 0
    for i in result:
        sum_of_elements = sum_of_elements + i
    predictive_preference = 0
    for i in range(5):
        predictive_preference = predictive_preference + (result[4-i] * (i+1))
    predictive_preference = (predictive_preference / sum_of_elements)
    return predictive_preference


def main():

    input_list = []
    choice = ""
    choice = raw_input("\nDo you want to use the EXISTING SIMPLE DB ? (y/n) :")
    if((choice == 'y') | (choice == 'Y')):
        input_list = main_table.use_existing_db()
    else:
        input_list = main_table.create_new_simple_db()

    users = input_list[0]
    objective_users = input_list[1]
    subjective_users = input_list[2]
    active_user = input_list[3]
    items = input_list[4]
    data_base = input_list[5]
    preference_rating = main_table.pref_rating

    #print "\nusers--", users
    #print "\nitems--", items
    #print "\nsubjective_users--", subjective_users
    #print "\nobjective_users--", objective_users
    #print "\nactive_user--", active_user
    #print "\ndatabase", data_base

    null_item = get_null_item(active_user, data_base)
    similarity = {}
    if(null_item == 0):
        print "\nNo NULL entry is found for active user."
    else:
        # Get the similarities of users
        for user in users:
            if(user != active_user):
                similarity[user] = get_similarity(user, active_user, items, preference_rating, data_base)
        print "\nAll Similarities--\n",similarity
        # Get the top3 values and keys
        top3_similarity_keys = get_top3_keys(similarity)
        top3_similarity_values = get_top3_values(similarity)
        print "\nTop 3 similarities--\n",top3_similarity_keys

        # Get the preference matrix
        preference_matrix = get_pref_matrix(top3_similarity_keys, preference_rating, null_item, data_base)
        print "\nPreference Matrix--\n",preference_matrix

        # Get the Normalized similarities of the top3 users
        normalized_similarities = get_normalized_similarities(top3_similarity_values)
        print "\nNormalized similarities--\n", normalized_similarities

        # Get the predictive preference value
        predictive_preference = get_predictive_precedence(normalized_similarities,preference_matrix)
        print "\nPredictive preference--\n", predictive_preference

        # Round of the predictive preference value
        predictive_preference = math.floor(predictive_preference)

        # Update the database
        data_base[active_user][null_item] = main_table.predictive_rating[predictive_preference]

        # Display the updated Database
        print "\nDatabase--"
        for i in sorted(users):
            print  i,data_base[i]
main()