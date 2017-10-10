# coding: utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import cx_Oracle
import requests
import time
import sys
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

# 创建一个logger
logger = logging.getLogger('smjjgs')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('smjjgs.log')
fh.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)

logger.info('start smjjgs')



# alc = create_engine(engine, echo=False)



# 获取管理人链接及链接id
def get_manager_url_list(driver):
    href_list = driver.find_elements_by_xpath("//td/a[contains(@href, 'html')]")
    id_list = []  # 链接
    # print len(href_list)
    for href in href_list:
        href_text = href.get_attribute('href');
        if "manage" in href_text:
            test =1;
        else:
            url = href.get_attribute('href')
            begin_idx = url.rfind('/')
            end_idx = url.rfind('.html')
            if begin_idx == -1 or end_idx == -1:
                continue
            id = url[begin_idx + 1:end_idx]
            id_list.append(int(id))
    return id_list


# 查询管理人所有页码的数据
def get_manager_page_list(driver):
    driver.find_element_by_css_selector("option[value=\"100\"]").click()  # 每页显示100条记录
    time.sleep(2)
    page_info = driver.find_element_by_css_selector("div[id=\"fundlist_info\"]").text
    idx = page_info.rfind('共')
    if idx == -1:
        print page_info
        return None

    max_page = int(page_info[idx + 1:-1])  # 页数
    id_list = get_manager_url_list(driver)  # 获取第一页的链接和ID
    get_grade(id_list);
    if max_page == 1:
        return id_list
    for i in range(1, max_page):
        time.sleep(5)
        driver.find_element_by_css_selector("a[class=\"paginate_button next\"]").click()  # 翻页
        time.sleep(2)
        tmp_list = get_manager_url_list(driver)
        get_grade(tmp_list);
    return id_list

# 获取单个链接中网页的内容
def get_grade(id_list):
    for i in range(0,len(id_list)):
        try:
            url = "http://gs.amac.org.cn/amac-infodisc/res/pof/fund/%s.html" % (id_list[i])
            resp = requests.get(url);
            resp.encoding = 'utf-8';
            soup = BeautifulSoup(resp.text);
            grades = soup.select("td.td-content");
            contents = [];
            for grade in grades:
                grade_text = grade.get_text();
                grade_text = grade_text.encode('utf-8');
                grade_text = grade_text.replace("'", "''");
                contents.append(grade_text);
            if len(contents) > 0:
                if len(contents) < 18:
                    for ii in range(17):
                        contents.append("");
                sql = "INSERT INTO PIF.TPIF_PC_SMJJGSXX(ID,JJMC,JJBH,CLSJ,BASJ,JJBAJD,JJLX,BZ,JJGLRMC,GLLX,TGRMC,ZYTZLY,YZZT,JJXXZHGXSJ,JJXHTBTS,YB,BNB,NB,JB,CZRQ)VALUES(CRMII.FUNC_NEXTID('TPIF_PC_SMJJGSXX'),'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s)" % (
                contents[0], contents[1], contents[2], contents[3], contents[4], contents[5], contents[6], contents[7],
                contents[8], contents[9], contents[10], contents[11], contents[12], contents[13], contents[14],
                contents[15], contents[16], contents[17],"to_char(sysdate,'yyyymmdd')");
                cursor.execute(sql);
                db.commit();
        except Exception,e:
            print e
            print "%s"% (sql)
            logger.error(e);
            logger.error("%s"% (sql));
    return 1

# 获取所有基金的链接和link_id
def get_all_managers():
    # driver = webdriver.Firefox(executable_path = 'C:/Program Files (x86)/Mozilla Firefox/geckodriver')
    driver = webdriver.PhantomJS()

    url = 'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html'
    driver.get(url)

    time.sleep(6)
    str_close = "button[class=\"ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only\"]"
    driver.find_element_by_css_selector(str_close).click()  # 点关闭
    id_list = get_manager_page_list(driver)  # 查询所有
    driver.close()
    return id_list


if __name__ == "__main__":
    try:
        # # 数据库
        usr = "pif"
        pwd = "pif"
        host = "172.70.0.45:1521/pif"
        engine = "oracle://" + usr + ":" + pwd + "@" + host
        #
        os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
        db = cx_Oracle.connect(usr, pwd, host)
        cursor = db.cursor()
        cursor.execute("TRUNCATE TABLE PIF.TPIF_PC_SMJJGSXX");
        db.commit();
        id_list = get_all_managers()  # 链接信息
        cursor.close()
        db.close()
        logger.info('success smjjgs');
    except Exception,e:
        logger.error(e);
#     df = pd.DataFrame(map(list, zip(*arr)), columns=manager_link_cols)
#     date = str(time.strftime('%Y%m%d', time.localtime(time.time())))  # 日期
# df["UPDATE_DATE"] = [date] * df.shape[0]
# df.to_sql("tb_smjj_link_id", alc, if_exists='append', index=False)  # 入库



