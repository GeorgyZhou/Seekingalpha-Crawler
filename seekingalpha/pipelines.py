# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb as mdb
from spiders.log import *
from scrapy.utils.project import  get_project_settings

class SeekingalphaPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        self.conn = mdb.connect(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql_url = self.sql_field_map(item['url'])
        sql_article_id = self.sql_field_map(item['article_id'])
        sql_article_date = self.sql_field_map(item['article_date'])
        sql_article_title = self.sql_field_map(item['article_title'])
        sql_article_text = self.sql_field_map(item['article_text'])
        sql_article_raw = self.sql_field_map(item['article_raw'])
        sql_author = self.sql_field_map(item['author'])
        sql_author_id = self.sql_field_map(item['author_id'])
        sql_stock_name = self.sql_field_map(item['stock_name'])
        sql_stock_id = self.sql_field_map(item['stock_id'])
        sql_disclosure = self.sql_field_map(item['disclosure'])
        sql = ('INSERT INTO short_articles(url, article_id, article_date, article_title, article_text, article_raw, ' +
              'author, author_id, stock_name, stock_id, disclosure) VALUES ("%s", %s, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' %
               (sql_url, sql_article_id, sql_article_date, sql_article_title, sql_article_text, sql_article_raw, sql_author, sql_author_id,
                sql_stock_name, sql_stock_id, sql_disclosure))
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            info('SQL INSERT COMMIT!')
        except mdb.Error as e:
            warn("Error %d: %s" % (e.args[0], e.args[1]))
            return item

    def sql_field_map(self, field):
        return 'NULL' if not field else mdb.escape_string(field)