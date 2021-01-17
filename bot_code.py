import tweepy
import random, os
from google.cloud import storage

storage_client = storage.Client()
bucket_name = os.getenv('bucket_name')

def take_rand_num_enem():
    rand_num = str(random.randrange(136, 181))

    return rand_num

def take_rand_num_fuvest(rand_year):
    rand_num = ''
    # questions from 1 to 10
    if rand_year in ['2009','2010','2011']:
        rand_num = str(random.randrange(1,11))
    # questions from 1 to 12
    elif rand_year == '2014':
        rand_num = str(random.randrange(1,13))
    # questions from 1 to 11
    else:
        rand_num = str(random.randrange(1,12))

    return rand_num

def take_rand_num_unicamp(rand_year):
    rand_num = ''
    # year < 2010
    if rand_year == '2009':
        rand_year = random.choice(('2010','2011','2012','2013','2014','2015','2016','2017','2018','2019'))
        rand_num = take_rand_num_unicamp(rand_year)
    elif rand_year in ['2010','2011','2012']:
        rand_num = str(random.randrange(1,11))
    elif rand_year == '2013':
        rand_num = str(random.randrange(1,13))
    elif rand_year in ['2014','2015','2016']:
        rand_num = str(random.randrange(1,15))
    else:
        rand_num = str(random.randrange(1,14))

    return rand_num

def take_rand_num_vunesp(rand_year,rand_half):
    rand_num = ''
    if rand_year in ['2009','2012','2013','2015','2016','2018'] and rand_half == '':
        rand_num = str(random.randrange(1,8))
    elif rand_year in ['2011', '2013', '2016'] and rand_half == 'meio':
    	rand_num = str(random.randrange(1,8))
    else:
    	rand_num = str(random.randrange(1,9))

    return rand_num

def run_bot(request):
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_KEY'), os.getenv('ACCESS_SECRET'))
    api = tweepy.API(auth)

    rand_exam = random.choice(('enem','fuvest', 'unicamp', 'vunesp'))
    rand_year = random.choice(('2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019'))
    
    rand_half = ''

    if rand_exam == 'vunesp' and int(rand_year) < 2018:
        rand_half = random.choice(('_meio',''))

    switcher = {
        'enem': take_rand_num_enem(),
        'fuvest': take_rand_num_fuvest(rand_year),
        'unicamp': take_rand_num_unicamp(rand_year),
        'vunesp': take_rand_num_vunesp(rand_year,rand_half)
    }

    rand_num = switcher.get(rand_exam)

    blob_question = storage_client.bucket(bucket_name).blob(rand_exam + '/'+ rand_year + rand_half + '/q_' + rand_num + '.png')
    blob_question.download_to_filename('/tmp/question.png')    

    status = "Aproveite que você está no twitter e responda essa questão {exame} {half} {year}.".format(exame="do " + rand_exam.upper() if rand_exam == "enem" else "da " + rand_exam.upper(), half= rand_half if rand_half == '' else 'MEIO DE ANO', year= rand_year if rand_exam == "enem" else str(int(rand_year)+1))

    status_obj_p = api.update_with_media(filename='/tmp/question.png', status=status)
