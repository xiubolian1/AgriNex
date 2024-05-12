SECRET_KEY = "agha151gf15"
# 数据库的配置
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'flask_potato'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 邮箱授权码  邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL = True
MAIL_PORT = 465
#要发送的邮箱
MAIL_USERNAME = "2650862699@qq.com"
#SMTP授权码，具体开通步骤可进行百度,下条默认是失效的
MAIL_PASSWORD = "hspbucaoywyoecde"
#默认发送地址，与第一条保持不变
MAIL_DEFAULT_SENDER = '2650862699@qq.com'


ALLOWED_EXTENSIONS = set(["png", "jpg", "JPG", "PNG", "bmp", "jpeg"])
UPLOAD_FOLDER = 'uploads/'
UPLOAD_AVATAR_FOLDER = 'uploads/avatar/'

img_adjusts = {
"Rust":'锈病（Rust）：病害管理：及时清除感染的叶子和植株部分，以减少病害传播。化学控制：使用合适的杀菌剂进行喷洒，根据农业专家的建议选择适当的化学品，并确保按照标签说明正确使用。植物健康：加强植物的养分供应，保持其健康和抵抗力，有助于减少病害的发生和传播。',
"Slug":'蛞蝓病（Slug）：清洁措施：定期清除植物周围的杂草和积水，因为它们可能会成为蛞蝓的栖息地。物理控制：在受影响的区域放置蛞蝓诱捕器或使用其他物理控制方法，如蛞蝓捕捉器或障碍物。天敌引入：引入天敌如蛞蝓的天敌，如甲壳类动物或鸟类，以帮助控制蛞蝓数量。',
"Curl":'卷叶病（Curl）：病害管理：定期检查植物，并及时移除受感染的叶子，以减少病害的传播。灌溉控制：避免叶面直接浇水，尤其是在晴天的时候，因为叶面湿润有助于病害的传播。气候管理：保持适宜的空气循环和湿度，避免植物长时间处于潮湿环境中，可以减少卷叶病的发生。',

}
