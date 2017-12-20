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
            if((uj_r != "") & (uk_r != "")):
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
            return round(similarity,2)
    except:
        pass

# Function to compute the preference matrix from the top3 users
def get_pref_matrix(top3, pref_rating, null_item, db):
    p_matrix = []
    for i in range(4):
         p_matrix.append(pref_rating[db[top3[i]][null_item]])
    return p_matrix

# Function to compute the normalized similarities of the top3 users
def get_normalized_similarities(top3_similarities):
    sum_of_similarities = 0
    for i in top3_similarities:
        sum_of_similarities = sum_of_similarities + i
    return [round(val / sum_of_similarities, 2) for val in top3_similarities]

# Function to compute the predictive precedence value
def get_predictive_precedence(normalized_similarities, preference_matrix):

    # Function to multiply two matrices
    def matrix_multiply(normalized_similarities, preference_matrix):
        matrix_mul = [0,0,0,0,0]
        try:
            for i in range(5):
                matrix_mul[i] = 0
                for j in range(4):
                    matrix_mul[i] = matrix_mul[i] + (normalized_similarities[j] * preference_matrix[j][i])
            return matrix_mul
        except Exception as e:
            pass

    result = matrix_multiply(normalized_similarities, preference_matrix)
    sum_of_elements = 0
    for i in result:
        sum_of_elements = (sum_of_elements + i)
    predictive_preference = 0
    for i in range(5):
        predictive_preference = (predictive_preference + (result[4-i] * (i+1)))
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
    threshold = 0.15

    #Calculate the average rating of each item rated by subjective user.
    sub_user_rating = {}
    count_su = len(subjective_users)
    for item in items:
        sub_user_rating[item] = 0
        for su in subjective_users:
            sub_user_rating[item] += main_table.pref_values[data_base[su][item]]
        temp = round((sub_user_rating[item] / count_su),1)
        decimal = (temp - math.floor(temp))
        if(decimal > 0.75):
            temp = math.ceil(temp)
        elif(decimal < 0.26):
            temp = math.floor(temp)
        else:
            temp = math.floor(temp) + 0.5
        sub_user_rating[item] = main_table.predictive_rating[temp]
    print "\nAverage Subjective user similarity--\n", sub_user_rating
    data_base['us'] = sub_user_rating

    # Calculate the similarities between the subjective user and every other user and create a ranking list.
    ranking_list = {}
    similarity_difference = {}
    for user in objective_users:
        ranking_list[user] = get_similarity(user, 'us', items, preference_rating, data_base)
    print "\nRanking_list--\n",ranking_list

    #get the similarities above the threshold value
    null_item = get_null_item(active_user, data_base)
    similarity = {}
    if(null_item == 0):
        print "\nNo NULL entry is found for active user."
    else:
        similarity_keys = []
        similarity_values = []
        # Get the similarities of users
        for user in users:
            if((user not in active_user) & (user not in subjective_users)):
                try:
                    similarity_difference[user] = round(abs(ranking_list[user] - ranking_list[active_user]),2)
                    if (similarity_difference[user] <= threshold):
                        similarity_keys.append(user)
                        similarity[user] = get_similarity(user, active_user, items, preference_rating, data_base)
                        similarity_values.append(similarity[user])
                except:
                    pass

        print "\nSimilarity-Differences--\n",similarity_difference
        print "\nSimilarities users above threshold--\n",similarity_keys
        print "\nSimilarities values above threshold--\n",similarity_values

        top3_values = sorted(similarity_values,reverse=True)[:3]
        top3_keys = [user for user in similarity.keys() if similarity[user] in top3_values]

        print "\nTop3 values--\n", top3_values
        print "\nTop3 keys--\n", top3_keys

        top3_keys.append('us')
        # Get the preference matrix
        preference_matrix = get_pref_matrix(top3_keys, preference_rating, null_item, data_base)
        print "\nPreference Matrix--\n",preference_matrix

        # Get the Normalized similarities of the top3 users
        normalized_similarities = get_normalized_similarities(similarity_values)
        print "\nNormalized similarities--\n", normalized_similarities

        # Get the predictive preference value
        predictive_preference = get_predictive_precedence(normalized_similarities,preference_matrix)
        print "\nPredictive preference--\n", predictive_preference

        # Round of the predictive preference value
        temp = predictive_preference
        decimal = (temp - math.floor(temp))
        if(decimal > 0.75):
            temp = math.ceil(temp)
        elif(decimal < 0.26):
            temp = math.floor(temp)
        else:
            temp = math.floor(temp) + 0.5
        predictive_preference = main_table.predictive_rating[temp]

        # Update the database
        data_base[active_user][null_item] = predictive_preference

        # Display the updated Database
        print "\nDatabase--"
        for i in sorted(users):
            print  i,data_base[i]
main()