{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "App.py",
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyNgqi78H0iz+I/mNvCSnhtk",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/shweta7122/Recommender/blob/main/App.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "NP0tenTlKbfK"
      },
      "source": [
        "!pip install streamlit"
      ],
      "execution_count": 1,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "-pyzZTVFKSIG"
      },
      "source": [
        "import streamlit as st\n",
        "import warnings\n",
        "warnings.filterwarnings(\"ignore\")\n",
        "# EDA Pkgs\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "import pandas as pd\n",
        "import tweepy\n",
        "import json\n",
        "from tweepy import OAuthHandler\n",
        "import re\n",
        "import textblob\n",
        "from textblob import TextBlob\n",
        "from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator\n",
        "import openpyxl\n",
        "import time\n",
        "import tqdm"
      ],
      "execution_count": 2,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "UUV3UGHCKrFJ"
      },
      "source": [
        "#To Hide Warnings\n",
        "st.set_option('deprecation.showfileUploaderEncoding', False)\n",
        "st.set_option('deprecation.showPyplotGlobalUse', False)\n",
        "# Viz Pkgs\n",
        "import matplotlib.pyplot as plt\n",
        "import matplotlib\n",
        "matplotlib.use('Agg')\n",
        "import seaborn as sns\n",
        "#sns.set_style('darkgrid')\n",
        "import tweepy\n",
        "from textblob import TextBlob\n",
        "from wordcloud import WordCloud\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "import re\n",
        "import matplotlib.pyplot as plt\n",
        "plt.style.use('fivethirtyeight')"
      ],
      "execution_count": 98,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "uXT8EvkfKx87"
      },
      "source": [
        "STYLE = \"\"\"\n",
        "<style>\n",
        "img {\n",
        "    max-width: 100%;\n",
        "}\n",
        "</style> \"\"\"\n"
      ],
      "execution_count": 99,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "CzY_j1NWK2Gj"
      },
      "source": [
        "def main():\n",
        "    \"\"\" Common ML Dataset Explorer \"\"\"\n",
        "    #st.title(\"Live twitter Sentiment analysis\")\n",
        "    #st.subheader(\"Select a Twitter Handle for which you'd like to get the sentiment analysis:\")\n",
        "\n",
        "    html_temp = \"\"\"\n",
        "\t<div style=\"background-color:tomato;\"><p style=\"color:white;font-size:25px;padding:9px\">Live twitter Sentiment analysis</p></div>\n",
        "\t\"\"\"\n",
        "    st.markdown(html_temp, unsafe_allow_html=True)\n",
        "    st.subheader(\"Select a Twitter Handle which you'd like to get the sentiment analysis on :\")\n"
      ],
      "execution_count": 1,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "01dLTozPLFYz"
      },
      "source": [
        "################# Twitter API Connection #######################\n",
        "consumerKey = \"kDgO0qZRdVkKICung7MkPl2QU\"\n",
        "consumerSecret = \"ZOQhlwSEMhZUtdVPjc9CG4kaGCEWdR6AT9e2SJiJXoIMHxnIDi\"\n",
        "accessToken = \"1445776538599768074-Vl3Udixl0J4EwIokYsboiQYbkviqin\"\n",
        "accessTokenSecret = \"9xBgvVedGyrtUsofSvVLqM9i499AfSoapl0XtBzaVamrL\""
      ],
      "execution_count": 76,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "G1lSxe_WLe-8"
      },
      "source": [
        "# Creating the authentication data\n",
        "authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)\n",
        "\n",
        "# Set the access token and access token secret\n",
        "authenticate.set_access_token(accessToken, accessTokenSecret)\n",
        "\n",
        "# Create the API object\n",
        "api = tweepy.API(authenticate, wait_on_rate_limit=True)"
      ],
      "execution_count": 100,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "TylcnH1XMEHI"
      },
      "source": [
        "TwitterHandle = \"JustinTrudeau\"\n",
        "posts = api.user_timeline(screen_name = TwitterHandle, count = 100, lang ='en', tweet_mode=\"extended\")\n",
        "df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])"
      ],
      "execution_count": 102,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "vby7eYEUEYm4"
      },
      "source": [
        "# Create a function to clean the texts\n",
        "def cleanTxt(text):\n",
        "  text = re.sub(r'@[A-Za-z0-9]+', '', text) #Removed @mentions\n",
        "  text = re.sub(r'#', '', text) #Removed Hastags\n",
        "  text = re.sub(r'RT[\\s]+', '', text) #Removed RT\n",
        "  text = re.sub(r'https?:\\/\\/\\S+', '', text) # Removed hyperlinks\n",
        "\n",
        "  return text"
      ],
      "execution_count": 79,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "6n4eKzD4Gbg9"
      },
      "source": [
        "# Create a function to get the functionality\n",
        "def getSubjectivity(text):\n",
        "  return TextBlob(text).sentiment.subjectivity\n",
        "\n",
        "# Create a function to get the polarity\n",
        "def getPolarity(text):\n",
        "  return TextBlob(text).sentiment.polarity\n",
        "\n",
        "# Create two new columns\n",
        "df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)\n",
        "df['Polarity'] = df['Tweets'].apply(getPolarity)\n"
      ],
      "execution_count": 81,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "dy6KSIkcHKAw"
      },
      "source": [
        "# Create a function to compute the sentiment analysis\n",
        "def getAnalysis(score):\n",
        "  if score < 0:\n",
        "    return 'Negative'\n",
        "  elif score == 0:\n",
        "    return 'Neutral'\n",
        "  else:\n",
        "    return 'Positive'\n",
        "\n",
        "df['Analysis'] = df['Polarity'].apply(getAnalysis)\n"
      ],
      "execution_count": 82,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "ZJLR0QcIGgbr"
      },
      "source": [
        "from subprocess import check_output\n",
        "from wordcloud import WordCloud, STOPWORDS\n",
        "stopwords = set(STOPWORDS)"
      ],
      "execution_count": 83,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Cv92-vEEGlUN",
        "outputId": "1f1a8051-a3a6-4b92-c323-63fc8ce23282"
      },
      "source": [
        "allWords = ' '.join( [twts for twts in df['Tweets']])\n",
        "wordcloud = WordCloud(background_color='white', width=500, height=300, stopwords=stopwords,max_words=50, max_font_size=120, random_state=21).generate(allWords)\n",
        "\n",
        "print(wordcloud)\n",
        "fig = plt.figure(1, figsize=(15,12))\n",
        "plt.imshow(wordcloud, interpolation = 'bilinear')\n",
        "plt.axis('off')\n",
        "plt.show()\n",
        "fig.savefig(\"word1.png\", dpi=100)"
      ],
      "execution_count": 84,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "<wordcloud.wordcloud.WordCloud object at 0x7fc96b05a810>\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "hPPm1bdmKXAh",
        "outputId": "5a03ddb9-13bf-41c2-ebbe-2e78b35cb361"
      },
      "source": [
        "from PIL import Image\n",
        "image = Image.open('logo.jpg')\n",
        "st.image(image, caption='Twitter for Analytics',use_column_width=True)"
      ],
      "execution_count": 87,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "2021-10-07 19:15:04.455 \n",
            "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
            "  command:\n",
            "\n",
            "    streamlit run /usr/local/lib/python3.7/dist-packages/ipykernel_launcher.py [ARGUMENTS]\n"
          ]
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "DeltaGenerator(_root_container=0, _provided_cursor=None, _parent=None, _block_type=None, _form_data=None)"
            ]
          },
          "metadata": {},
          "execution_count": 87
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "IXc4ChR-Kigg"
      },
      "source": [
        "# Collect Input from user :\n",
        "TwitterHandle = str()\n",
        "TwitterHandle = str(st.text_input(\"Enter the TwitterHandle you are interested in (Press Enter once done)\"))     \n",
        "    \n",
        "if len(TwitterHandle) > 0 :\n",
        "        # Call the function to extract the data. pass the Twitter Handle and filename you want the data to be stored in.\n",
        "        with st.spinner(\"Please wait, Tweets are being extracted\"):\n",
        "            get_tweets(TwitterHandle , Count=200)\n",
        "        st.success('Tweets have been Extracted !!!!')    \n",
        "           \n",
        "    \n",
        "        # Call function to get Clean tweets\n",
        "        df['CleanTxt'] = df['Tweets'].apply(lambda x : cleanTxt(x))\n",
        "    \n",
        "        # Call function to get the Sentiments\n",
        "        df[\"Polarity\"] = df[\"Tweet\"].apply(lambda x : getAnalysis(x))\n",
        "        \n",
        "        \n",
        "        # Write Summary of the Tweets\n",
        "        st.write(\"Total Tweets Extracted for the User '{}' are : {}\".format(TwitterHandle,len(df.Tweets)))\n",
        "        st.write(\"Total Positive Tweets are : {}\".format(len(df[df[\"Analysis\"]==\"Positive\"])))\n",
        "        st.write(\"Total Negative Tweets are : {}\".format(len(df[df[\"Analysis\"]==\"Negative\"])))\n",
        "        st.write(\"Total Neutral Tweets are : {}\".format(len(df[df[\"Analysis\"]==\"Neutral\"])))\n",
        "        \n",
        "        # See the Extracted Data : \n",
        "        if st.button(\"See the Extracted Data\"):\n",
        "            #st.markdown(html_temp, unsafe_allow_html=True)\n",
        "            st.success(\"Below is the Extracted Data :\")\n",
        "            st.write(df.head(50))\n",
        "        \n",
        "        \n",
        "        # get the countPlot\n",
        "        if st.button(\"Get Count Plot for Different Sentiments\"):\n",
        "            st.success(\"Generating A Count Plot\")\n",
        "            st.subheader(\" Count Plot for Different Sentiments\")\n",
        "            st.write(sns.countplot(df[\"Analysis\"]))\n",
        "            st.pyplot()\n",
        "        \n",
        "        # Piechart \n",
        "        if st.button(\"Get Pie Chart for Different Sentiments\"):\n",
        "            st.success(\"Generating A Pie Chart\")\n",
        "            a=len(df[df[\"Analysis\"]==\"Positive\"])\n",
        "            b=len(df[df[\"Analysis\"]==\"Negative\"])\n",
        "            c=len(df[df[\"Analysis\"]==\"Neutral\"])\n",
        "            d=np.array([a,b,c])\n",
        "            explode = (0.1, 0.0, 0.1)\n",
        "            st.write(plt.pie(d,shadow=True,explode=explode,labels=[\"Positive\",\"Negative\",\"Neutral\"],autopct='%1.2f%%'))\n",
        "            st.pyplot()\n",
        "            \n",
        "       \n",
        "        \n",
        "        ## Points to add 1. Make Backgroud Clear for Wordcloud 2. Remove keywords from Wordcloud\n",
        "        \n",
        "        \n",
        "        # Create a Worlcloud\n",
        "        if st.button(\"Get WordCloud for{}\".format(TwitterHandle)):\n",
        "            st.success(\"Generating A WordCloud for all tweets by {}\".format(TwitterHandle))\n",
        "            text = \" \".join(review for review in df.cleanTxt)\n",
        "            stopwords = set(STOPWORDS)\n",
        "            text_newALL = prepCloud(text,TwitterHandle)\n",
        "            wordcloud = WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_newALL)\n",
        "            st.write(plt.imshow(wordcloud, interpolation='bilinear'))\n",
        "            st.pyplot()\n",
        "        \n",
        "        \n",
        "        #Wordcloud for Positive tweets only\n",
        "        if st.button(\"Get WordCloud for all Positive Tweets by {}\".format(TwitterHandle)):\n",
        "            st.success(\"Generating A WordCloud for all Positive Tweets by {}\".format(TwitterHandle))\n",
        "            text_positive = \" \".join(review for review in df[df[\"Analysis\"]==\"Positive\"].cleanTxt)\n",
        "            stopwords = set(STOPWORDS)\n",
        "            text_new_positive = prepCloud(text_positive,TwitterHandle)\n",
        "            #text_positive=\" \".join([word for word in text_positive.split() if word not in stopwords])\n",
        "            wordcloud = WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_new_positive)\n",
        "            st.write(plt.imshow(wordcloud, interpolation='bilinear'))\n",
        "            st.pyplot()\n",
        "        \n",
        "        \n",
        "        #Wordcloud for Negative tweets only       \n",
        "        if st.button(\"Get WordCloud for all Negative Tweets by {}\".format(TwitterHandle)):\n",
        "            st.success(\"Generating A WordCloud for all Positive Tweets by {}\".format(TwitterHandle))\n",
        "            text_negative = \" \".join(review for review in df[df[\"Analysis\"]==\"Negative\"].cleanTxt)\n",
        "            stopwords = set(STOPWORDS)\n",
        "            text_new_negative = prepCloud(text_negative,TwitterHandle)\n",
        "            #text_negative=\" \".join([word for word in text_negative.split() if word not in stopwords])\n",
        "            wordcloud = WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_new_negative)\n",
        "            st.write(plt.imshow(wordcloud, interpolation='bilinear'))\n",
        "            st.pyplot()\n",
        "        \n"
      ],
      "execution_count": 94,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "PF1Q4W_WRRJP"
      },
      "source": [
        "    st.sidebar.header(\"About App\")\n",
        "    st.sidebar.info(\"A Twitter Sentiment analysis Project -CSDA1040\")\n",
        "    st.sidebar.text(\"Built with Streamlit\")\n",
        "\n",
        "    #st.sidebar.subheader(\"Scatter-plot setup\")\n",
        "    #box1 = st.sidebar.selectbox(label= \"X axis\", options = numeric_columns)\n",
        "    #box2 = st.sidebar.selectbox(label=\"Y axis\", options=numeric_columns)\n",
        "    #sns.jointplot(x=box1, y= box2, data=df, kind = \"reg\", color= \"red\")\n",
        "    #st.pyplot()\n",
        "\n",
        "\n",
        "\n",
        "    if st.button(\"Exit\"):\n",
        "        st.balloons()"
      ],
      "execution_count": 95,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "s_uF-zYGRWO_"
      },
      "source": [
        "if __name__ == '__main__':\n",
        "    main()"
      ],
      "execution_count": 96,
      "outputs": []
    }
  ]
}