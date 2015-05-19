#!/usr/bin/env python
# coding=utf-8

import os
import time

DEFAULT_AUTHOR = "大饼"
DEFAULT_SUMMARY = "通过手机上传"
URL_PREFIX = "http://www.42kr.com/podcast/"
XML_FILE_PATH = "/home/Cake/site/42kr/feed.xml"
SUBMIT_FOLDER = "/home/Cake/tool/podcast_submit/submit_folder/"
PODCAST_FOLDER = "/home/Cake/site/42kr/podcast/"

class Podcast(object):

    def __init__(self, filename, author, summary, url, mediaType = "audio/mpeg"):
        self.filename = filename
        self.title = time.strftime("%Y-%m-%d %H:%M:%S")
        self.author = author
        self.subtitle = filename[:-4]
        self.summary = summary
        self.url = url
        self.mediaType = mediaType
        self.pubDate = time.strftime("%a, %d %b %Y %H:%M:%S CST")

    def toRSS(self):
        self.content = "<item>\n"
        self.content += "<title>%s</title>\n" % self.title
        self.content += "<itunes:author>%s</itunes:author>\n" % self.author
        self.content += "<itunes:subtitle>%s</itunes:subtitle>\n" % self.subtitle
        self.content += "<itunes:summary>%s</itunes:summary>\n" % self.summary
        self.content += "<enclosure url=\"%s\" type=\"%s\" />\n" % (self.url, self.mediaType)
        self.content += "<pubDate>%s</pubDate>\n" % self.pubDate
        self.content += "</item>\n\n"

    def writeXML(self, xmlFilePath):
        xmlFile = open(xmlFilePath, "r")
        lines = xmlFile.readlines()
        xmlFile.close()
        lines.insert(-2, self.content)
        print lines
        xmlFile = open(xmlFilePath, "w")
        xmlFile.writelines(lines)
        xmlFile.close()

    def submitFile(self, submitPath, podcastPath):
        os.system("mv " + submitPath + self.filename + " " + podcastPath)

def submit(submitPath, podcastPath):
    pcList = []
    for filename in os.listdir(submitPath):
        if filename.endswith("mp3"):
            pcList.append(Podcast(filename, DEFAULT_AUTHOR, DEFAULT_SUMMARY, URL_PREFIX + filename))
    for pc in pcList:
        pc.toRSS()
        pc.writeXML(XML_FILE_PATH)
        pc.submitFile(submitPath, podcastPath)
    print pcList

def main():
    submit(SUBMIT_FOLDER, PODCAST_FOLDER)

if __name__ == "__main__":
    main()
