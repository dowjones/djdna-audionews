import os, requests, json
import news_repo, news_storage
from flask import Flask, render_template, url_for, abort

rootdir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)


# ##### Front-End Requests #####

@app.route('/', methods=['GET'])
def render_news():
    return render_template('news.html')


@app.route('/article/<articleid>')
def render_article(articleid):
    server_name = url_for('render_news', _external=True)
    req_url = server_name + 'api/article/' + articleid
    response = requests.get(req_url)
    if(response.status_code != 200):
        print("ERR Failed API Request for article {} using URL {}. \
            Returned HTTP status {}".format(articleid, req_url, response.status_code))
    else:
        article_obj = response.json()
        return render_template('viewarticle.html', article=article_obj)
    print("ERR authsite:main:render_article: Returning 404!")
    return abort(404)


# ##### API Requests #####

@app.route('/api/news/random', methods=['GET'])
def req_api_news_random():
    return news_repo.get_random_news()


@app.route('/api/news/related', methods=['GET'])
def req_api_news_related():
    # When using Elasticsearch, run a Cosine Similarity Query
    # Checkout the project https://github.com/miballe/djdna-snapshot2elasticsearch
    return news_repo.get_random_news()


@app.route('/api/article/<articleid>')
def req_api_article_content(articleid):
    article_obj = news_repo.get_article_by_an(articleid)
    if article_obj is None:
        return abort(404)
    return article_obj


@app.route('/api/article/<articleid>/_audiofilename')
def req_api_article_audiofilename(articleid):
    filename = "{}.mp3".format(articleid)
    filepath = rootdir + './static/article-audio/' + filename
    temp_item = {}
    try:
        index_item = news_repo.get_article_by_an(articleid)
        file_exists = news_storage.check_file_exists(filename)
        if file_exists:
            print("[newsapi] INFO The file {} was successfully found in the CS bucket.".format(filename))
            temp_item['filename'] = filename
        else:
            print("[newsapi] INFO The file {} needs to be generated using Text-to-Speech.".format(filename))
            ttsc = texttospeech.TextToSpeechClient()
            text2syn_dt = datetime.datetime.fromtimestamp(index_item['_source']['publication_datetime']/1000).strftime('%d-%m-%Y')
            text2syn_pre = '<speak>This audio reader article is provided to you by Dow Jones. \n\
                           Generated within the audio news reader demo application for retail investors.'
            text2syn_head = '<break time="1s"/>Published on <say-as interpret-as="date" format="dd-mm-yyyy" detail="1">{}</say-as> by {}'.format(text2syn_dt, index_item['_source']['publisher_name'])
            text2syn_title = '<break time="1s"/>' + index_item['_source']['title']
            text2syn_body = '<break time="1s"/>' + index_item['_source']['body']
            text2syn_post = '<break time="2s"/>End of the Audio Article.</speak>'
            text2syn_full = text2syn_pre + text2syn_head + text2syn_title + text2syn_body + text2syn_post
            synthesis_input = texttospeech.types.SynthesisInput(ssml=text2syn_full)
            voice = texttospeech.types.VoiceSelectionParams(
                language_code='en-US',
                ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
            audio_config = texttospeech.types.AudioConfig(
                audio_encoding=texttospeech.enums.AudioEncoding.MP3)
            response = ttsc.synthesize_speech(synthesis_input, voice, audio_config)
            print("[newsapi] INFO Speech-to-Text API response received")
            with open(filepath, 'wb') as out:
                out.write(response.audio_content)
            print("[newsapi] INFO Audio file {} was copied locally".format(filename))
            blob = bucket.blob(filename)
            blob.upload_from_filename(filepath)
            print("[newsapi] INFO Audio file {} was uploaded to bucket {}".format(filename, sc_audionews_bucket))

            temp_item['filename'] = filename
    except:
        print("ERR - {}".format(sys.exc_info()[0]))
        temp_item['filename'] = "no-article.mp3"
    print("[newsapi] INFO Ended req_api_article_audiofilename for article id {}".format(articleid))
    return json.dumps(temp_item)


if __name__ == '__main__':
    app.run(debug=True)
