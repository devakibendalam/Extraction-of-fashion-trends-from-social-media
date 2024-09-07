from flask import Flask, render_template, request
import pandas as pd
import regex as re
from operator import itemgetter
import string
import urllib
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from selenium import webdriver
d = pd.read_csv('sample.csv')

app = Flask(__name__)


@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')



#def basic_cleaning(query):
#    query = remove_irrelevant(query)
#    query = make_lowercase(query)
#    query = do_tokenization(query)
#    query = remove_stopwords(query)
#    query = do_lemmatization(query)
#    query = remove_small(query)
#    query = convert_to_string(query)
#    return query


#final_types = []

#for clothing in clothing_types:
#    clothing = basic_cleaning(clothing)
#    if clothing not in final_types:
#        final_types.append(clothing)

# def for_data_fun(some_text):
#    some_text = str(some_text)
#    some_text = some_text.lower()
#    if ('-women-') in some_text and '-men-' in some_text:
#        return 'both'
#    elif ('-women-') in some_text:
#        return 'women'
#    elif ('-men-') in some_text:
#        return 'men'


data = pd.read_json('p.json')
subdata = pd.read_csv('s.csv')


def for_fun(some_text):
    some_text = str(some_text)
    some_text = some_text.lower()
    if ('"women') in some_text:
        return 'women'
    elif ('"men') in some_text:
        return 'men'


subdata['gender'] = subdata['product_specifications'].apply(for_fun)
testsub = subdata[subdata['gender'].isin(['men', 'women'])]
testsub = testsub[
    ['brand', 'description', 'product_specifications', 'product_name', 'product_url', 'product_category_tree',
     'gender']]


def for_data_fun(some_text):
    some_text = str(some_text)
    some_text = some_text.lower()
    if ('-women-') in some_text and '-men-' in some_text:
        return 'both'
    elif ('-women-') in some_text:
        return 'women'
    elif ('-men-') in some_text:
        return 'men'


data['gender'] = data['url'].apply(for_data_fun)
main_df = data.drop_duplicates(subset=['title'], keep='first')
testing = main_df.loc[~main_df['gender'].isin(['men', 'both', 'women'])]


def something_doing(some_text):
    some_text = str(some_text)
    some_text = some_text.lower()
    if ('women') in some_text or ('woman') in some_text:
        return 'women'
    elif ('men') in some_text or ('man') in some_text:
        return 'men'
    return None


testing['gender'] = testing['product_details'].apply(something_doing)
final_testing = testing.loc[~testing['gender'].isin(['men', 'both', 'women'])]
final_testing['gender'] = final_testing['description'].apply(something_doing)
final_testing = final_testing.dropna(axis=0, subset=['gender'])
testing = testing.dropna(axis=0, subset=['gender'])
main_df = main_df.dropna(axis=0, subset=['gender'])
dfs = [main_df, testing, final_testing]
merged1 = pd.concat(dfs)
merged1.reset_index(inplace=True)
main_df = subdata.drop_duplicates(subset=['product_name'], keep='first')
testing = main_df.loc[~main_df['gender'].isin(['men', 'both', 'women'])]


def something_doing(some_text):
    some_text = str(some_text)
    some_text = some_text.lower()
    if (('-women-') in some_text or ('-woman-') in some_text) and (('-men-') in some_text or ('-man-') in some_text):
        return 'both'
    elif ('-men-') in some_text or ('-man-') in some_text:
        return 'men'
    elif ('-women-') in some_text or ('-woman-') in some_text:
        return 'women'
    return None


testing['gender'] = testing['product_url'].apply(something_doing)
final_testing = testing.loc[~testing['gender'].isin(['men', 'both', 'women'])]


def something_doing(some_text):
    some_text = str(some_text)
    some_text = some_text.lower()
    some_text = some_text.split(' ')
    if ('woman') in some_text or ('women') in some_text:
        return 'women'
    elif ('man') in some_text or ('men') in some_text:
        return 'men'
    return None


final_testing['gender'] = final_testing['description'].apply(something_doing)
final_testing = final_testing.dropna(axis=0, subset=['gender'])
testing = testing.dropna(axis=0, subset=['gender'])
main_df = main_df.dropna(axis=0, subset=['gender'])
dfs = [main_df, testing, final_testing]
merged2 = pd.concat(dfs)
merged2.reset_index(inplace=True)
merged2.rename(columns={'product_name': 'title', 'product_category_tree': 'category'}, inplace=True)
drop_columns = ['_id', 'actual_price', 'average_rating', 'crawled_at', 'discount', 'images', 'out_of_stock', 'pid',
                'selling_price']
data.drop(drop_columns, axis=1, inplace=True)


def remove_irrelevant(some_text):
    return re.sub('[^a-zA-Z]', ' ', some_text)


def make_lowercase(some_text):
    some_text = str(some_text).lower()
    if 't shirt' in some_text:
        some_text = some_text.replace('t shirt', 'tshirt')
    return some_text


nltk.download('punkt')


def do_tokenization(some_text):
    return word_tokenize(some_text)


nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


def remove_stopwords(token):
    return [item for item in token if item not in stop_words]


nltk.download('wordnet')
nltk.download('omw-1.4')
lemma = WordNetLemmatizer()


def do_lemmatization(token):
    return [lemma.lemmatize(word=w, pos='v') for w in token]


def remove_small(token):
    return [i for i in token if len(i) > 2]


def convert_to_string(token):
    return ' '.join(token)


def do_cleaning():
    merged1['ntitle'] = merged1['title'].apply(remove_irrelevant)
    merged2['ntitle'] = merged2['title'].apply(remove_irrelevant)
    merged1['ntitle'] = merged1['ntitle'].apply(make_lowercase)
    merged2['ntitle'] = merged2['ntitle'].apply(make_lowercase)
    merged1['ntitle'] = merged1['ntitle'].apply(do_tokenization)
    merged2['ntitle'] = merged2['ntitle'].apply(do_tokenization)
    merged1['ntitle'] = merged1['ntitle'].apply(remove_stopwords)
    merged2['ntitle'] = merged2['ntitle'].apply(remove_stopwords)
    merged1['ntitle'] = merged1['ntitle'].apply(do_lemmatization)
    merged2['ntitle'] = merged2['ntitle'].apply(do_lemmatization)
    merged1['ntitle'] = merged1['ntitle'].apply(remove_small)
    merged2['ntitle'] = merged2['ntitle'].apply(remove_small)
    merged1['ntitle'] = merged1['ntitle'].apply(convert_to_string)
    merged2['ntitle'] = merged2['ntitle'].apply(convert_to_string)


def document_cleaning():
    document_list['title'] = document_list['title'].apply(remove_irrelevant)
    document_list['title'] = document_list['title'].apply(make_lowercase)
    document_list['title'] = document_list['title'].apply(do_tokenization)
    document_list['title'] = document_list['title'].apply(remove_stopwords)
    document_list['title'] = document_list['title'].apply(do_lemmatization)
    document_list['title'] = document_list['title'].apply(remove_small)
    document_list['title'] = document_list['title'].apply(convert_to_string)


do_cleaning()
merged1.drop('index', axis=1, inplace=True)
merged2.drop('index', axis=1, inplace=True)
my_data = [merged1['title'], merged2['title']]
documents = pd.concat(my_data)
documents = documents.drop_duplicates()
document_list = pd.DataFrame(documents)
document_cleaning()
document_list.reset_index(inplace=True)
document_list.drop('index', axis=1, inplace=True)
final_result = []
for i in document_list.title:
    lst = i.split(' ')
    result = []
    for word in lst:
        my_word = wordnet.synsets(word)
        if len(my_word) == 0:
            result.append(word)
            continue
        for inner_word in my_word:
            for x in inner_word.lemma_names():
                result.append(x)
    final_result.append(' '.join(result))

clothing_types = ['Outer wear', 'Active wear', 'Swimwear', 'Legwear', 'Neckwear', 'Shawls', 'Bridal', 'Pant',
                  'Undergarments', 'Uniform', 'Knit', 'Lounge', 'Shirts', 'Blouses', 'Bottoms', 'Sleep', 'Resort',
                  'Mourning', 'Afternoon', 'Afghan', 'line coat', 'line skirt', 'Apron', 'Ankle length Pants', 'Anklet',
                  'Apache Tie', 'Armband', 'Babushka', 'Baby Bonnet', 'Baby bunting', 'Baby doll dress', 'Baggy pants',
                  'Ball Gown', 'Balmacaan', 'Bandana', 'Ballerina skirt', 'Barfly apparel', 'Barn jacket',
                  'Basque waistline', 'Barrow coat', 'Bathing cap', 'Bathing suit', 'Bathrobe', 'Beach Pajamas',
                  'Bed Jacket', 'Bell bottom pants', 'Bell Boy Jacket', 'Belt', 'Bermuda Shorts', 'Bertha collar',
                  'Bias Slip', 'Bias skirt', 'Bike Tards', 'Bikini', 'Bishop sleeve', 'Bisht', 'Blazer', 'Bloomers',
                  'Blouse', 'Blouson', 'Bodycon dress', 'Bomber jacket', 'Bootcut', 'Boots', 'Bow Tie', 'Boxers',
                  'Boyshorts', 'Bow tie', 'Bra', 'Brassiere', 'KnickerSet', 'Bralette', 'Briefs', 'Burkha',
                  'Business suit', 'Bustier', 'Bustle', 'Button down shirt', 'Cap', 'Cape', 'Capri Pants', 'Cardigan',
                  'Cargos', 'Car coat', 'Circle skirt', 'Cloche', 'Cloak', 'Cocktail dress', 'Corset', 'Crew neck',
                  'Crop top', 'Cufflinks', 'Divided skirt', 'Doublet', 'Drape front', 'Dress', 'Dressing Gown',
                  'Dress Shirt', 'Dupatta', 'Flannel shirt', 'French pantyhose', 'Full Slips', 'Fur coat', 'Gaghra',
                  'Gartini', 'Gilet', 'Girdle', 'Gloves', 'G string', 'Hat', 'Hawaiian shirt', 'Hijab', 'Hipster',
                  'Hoody', 'House coat', 'Jacket', 'Jeans', 'Jeggings', 'Jumper', 'Kimono', 'Knee high socks',
                  'Knickers', 'Kurta', 'Leggings', 'Leg warmer', 'Lehanga', 'Lingerie', 'Lounge wear', 'Lounge pants',
                  'Maternity wear', 'Maxi', 'Mittens', 'Nightgown', 'Nightwear', 'Niqab', 'Oilskin clothing',
                  'Overalls', 'Overskirt', 'Padded Bra', 'Pajama', 'Panty', 'Pantyhose', 'Pencil skirt', 'Petticoat',
                  'Photo tshirts', 'Pleated skirts', 'Polo', 'Poet sleeve', 'Polo Shirt', 'Poncho', 'Pull on clothes',
                  'Pullover', 'Push up Bras', 'Pyjamas', 'Rain Coat', 'Robe', 'Running shorts', 'Sari', 'Saree',
                  'Sarong', 'Sash', 'Scarf', 'Shawl', 'Shervani', 'Shirt', 'Shorts', 'Slip', 'Ski Pants', 'Skirt',
                  'Socks', 'Stockings', 'Stole', 'Straight pants', 'Straight skirt', 'Suit', 'Summer Cardigan',
                  'Surplice', 'Suspenders', 'Swacket', 'Sweater', 'Sweatshirt', 'Sweats', 'Sweep train',
                  'Swimming Costume', 'Swimming Shorts', 'Swimming Trunks', 'Tap pants', 'T-Shirt', 'Tank top', 'Thong',
                  'Tie', 'Tiered skirt', 'Tights', 'Top', 'Toreador pants', 'Tracksuit', 'Trainers', 'Treggings',
                  'Trench Coat', 'Trousers', 'Trumpet skirt', 'Trousseau', 'Tulip hemmed skirt', 'Tummy shaper',
                  'Tunic', 'Turban', 'Turtleneck', 'Tuxedo Jacket', 'Tuxedo', 'Twin set', 'Ulster', 'Underwear',
                  'Uniform', 'Union suit', 'Unitard', 'Veil', 'Vest', 'Waistcoat', 'Watteau', 'Windsor Tie',
                  'Wrap around skirt', 'Whorts', 'Wind Pants', 'Wrap coat', 'Wylie coat', 'Yoga Pants', 'Zip front top']


def basic_cleaning(query):
    query = remove_irrelevant(query)
    query = make_lowercase(query)
    query = do_tokenization(query)
    query = remove_stopwords(query)
    query = do_lemmatization(query)
    query = remove_small(query)
    query = convert_to_string(query)
    return query


final_types = []

for clothing in clothing_types:
    clothing = basic_cleaning(clothing)
    if clothing not in final_types:
        final_types.append(clothing)


def calculate_score(query, term):
    query = query.split(' ')
    term = term.split(' ')
    temp_matches = set(final_types).intersection(set(query))
    matches = set(temp_matches).intersection(set(term))
    if len(matches) > 0:
        return 80
    else:
        return 0


def find_sim_fuzz(query, n):
    results = []
    for x in range(len(final_result)):
        score = fuzz.token_set_ratio(query, final_result[x]) + calculate_score(query, final_result[x])
        results.append([score, x])
    result = sorted(results, key=itemgetter(0), reverse=True)
    final_results = []
    for x in result[:n]:
        final_results.append(document_list['title'][x[1]])
    return final_results


def fetch_results(result_term):
    result = dict
    result_list = []
    n1 = merged1.loc[merged1['ntitle'] == result_term].shape[0]
    n2 = merged2.loc[merged2['ntitle'] == result_term].shape[0]
    if n1 > 0:
        category = list(merged1.loc[merged1['ntitle'] == result_term, 'category'])[0]
        description = list(merged1.loc[merged1['ntitle'] == result_term, 'description'])[0]
        gender = list(merged1.loc[merged1['ntitle'] == result_term, 'gender'])[0]
        sub_category = list(merged1.loc[merged1['ntitle'] == result_term, 'sub_category'])[0]
        title = list(merged1.loc[merged1['ntitle'] == result_term, 'title'])[0]
        normal = list(merged1.loc[merged1['ntitle'] == result_term, 'actual_price'])[0]
        selling = list(merged1.loc[merged1['ntitle'] == result_term, 'selling_price'])[0]
        url = list(merged1.loc[merged1['ntitle'] == result_term, 'url'])[0]
        image = (list(merged1.loc[merged1['ntitle'] == result_term, 'images'])[0])
        image = image[0]
        category = string.capwords(category)
        description = string.capwords(description)
        gender = string.capwords(gender)
        sub_category = string.capwords(sub_category)
        title = string.capwords(title)
        result_list = []
        result_dict = {
            'title': title,
            'description': description,
            'gender': gender,
            'category': category,
            'sub_category': sub_category,
            'normal_price': normal,
            'selling_price': selling,
            'url': url,
            'image_url': image}
        result_list.append(result_dict)
        print(
            'Title: {}\nDescription: {}\nGender: {}\nCategory: {}\nSub-Category: {}\n\nMRP: Rs. {}\nDiscounted Price: Rs. {}\nLink: {}\n'.format(
                title, description, gender, category, sub_category, normal, selling, url))
        print()
        try:
            f = urllib.request.urlopen(image)
            figure(figsize=(2.5, 2.5), dpi=80)
            a = plt.imread(f, 0)
            plt.imshow(a)
            plt.axis('off')
            plt.show()
            print('\n')
        except:
            print("No image currently available")
    elif n2 > 0:
        category = list(merged2.loc[merged2['ntitle'] == result_term, 'category'])[0][2:-2]
        description = list(merged2.loc[merged2['ntitle'] == result_term, 'description'])[0]
        gender = list(merged2.loc[merged2['ntitle'] == result_term, 'gender'])[0]
        title = list(merged2.loc[merged2['ntitle'] == result_term, 'title'])[0]
        normal = list(merged2.loc[merged2['ntitle'] == result_term, 'retail_price'])[0]
        selling = list(merged2.loc[merged2['ntitle'] == result_term, 'discounted_price'])[0]
        url = list(merged2.loc[merged2['ntitle'] == result_term, 'product_url'])[0]
        image = (list(merged2.loc[merged2['ntitle'] == result_term, 'image'])[0].split(','))
        image = str(image[0][2:-1])
        category = string.capwords(category)
        description = string.capwords(description)
        gender = string.capwords(gender)
        title = string.capwords(title)
        result_list = []
        result_dict = {
            'title': title,
            'description': description,
            'gender': gender,
            'category': category,
            'normal_price': normal,
            'selling_price': selling,
            'url': url,
            'image_url': image}
        result_list.append(result_dict)
        # mapping(result_list)
        print(
            'Title: {}\nDescription: {}\nGender: {}\nCategory: {}\n\nMRP: Rs. {}\nDiscounted Price: Rs. {}\nLink: {}\n'.format(
                title, description, gender, category, normal, selling, url))
        print()
        try:
            f = urllib.request.urlopen(image)
            figure(figsize=(2.5, 2.5), dpi=80)
            a = plt.imread(f, 0)
            plt.imshow(a)
            plt.axis('off')
            plt.show()
            print('\n')
        except:
            print("No image currently available")
    else:
        return 'Not Found!'
    return result_list


def get_top_results(query, n):
    li = []
    print()
    print('Query: {}\n'.format(query))
    query = basic_cleaning(query)
    results = find_sim_fuzz(query, n)
    print("Displaying Top {} Results,\n".format(n))
    for result in range(0, len(results)):
        print("Result #{}\n".format(result + 1))
        result = fetch_results(results[result])
        li.append(*result)
    return li



# Step 1: Create a list of labeled keywords
def mapping(self, result_list):
    keywords = result_list
    
    # Step 2: Initialize Selenium
    driver = webdriver.Chrome()

    # Step 3-5: Search for products and extract information
    product_data = []
    for keyword in keywords:
        driver.get('https://www.flipkart.com/')
        search_box = driver.find_element_by_name('q')
        search_box.send_keys(keyword)
        search_box.submit()
        
        for product in driver.find_elements_by_xpath('//div[@class="_2kHMtA"]'):
            title = product.find_element_by_xpath('.//a[@class="_2mylT6"]/text()').text
            description = product.find_element_by_xpath('.//div[@class="_2mylT6"]/text()').text
            price = product.find_element_by_xpath('.//div[@class="_30jeq3 _1_WHN1"]/text()').text
            
            product_data.append({'keyword': keyword, 'title': title, 'description': description, 'price': price})
            
    # Step 6: Output the results
    for product in product_data:
        break
    driver.quit()


@app.route("/get_top_results", methods=['POST'])
def get_top_result():
    if request.method == 'POST':
        query = request.form['query']
        number = int(request.form['number_wanted'])
        result = get_top_results(query, number)
        return render_template('results.html', query=query, num_results=number, results=result)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
