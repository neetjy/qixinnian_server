import os
import tornado.web
import shortuuid
from model.image_cartoon_tool import handle
from utils import date_util
import handler.base as base
import oss2

class UploadHandler(base.BaseHandler):

    def post(self, *args, **kwargs):
        config_path = self.get_file_path()
        today = date_util.todaystr()
        parent_folder = config_path['root_folder']
        static_folder = config_path['static']
        dealed_path = config_path['temp']+'/'
        dealed_dir = os.path.join(parent_folder,dealed_path)
        self.uuidname = shortuuid.uuid()
        parent_path = os.path.join(parent_folder, static_folder, today)
        file_path = parent_path+'/'+self.uuidname
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        filesDict = self.request.files

        uploaded_files = filesDict.get('file', [])

        for uploaded_file in uploaded_files:
            # 获取文件信息
            file_info = uploaded_file['filename']
            file_content = uploaded_file['body']

            # 保存文件到服务器
            upload_path = os.path.join(file_path, file_info)
            with open(upload_path, "wb") as f:
                f.write(file_content)
        self.handler_image(upload_path,dealed_dir)
 
    def handler_image(self, file_path,dealed_dir):
        result_path = handle(file_path,dealed_dir)
        ACCESS_KEY_ID = 'LTAI5tEJz5eitpchxCBf4jLi'
        ACCESS_KEY_SECRET = 'XMzrbDGKpeC5CNXxbD6t2DvhExJPJJ'
        ENDPOINT = 'oss-cn-qingdao.aliyuncs.com'
        BUCKET_NAME = 'edu-gulii-1010123'

        # 初始化OSS客户端
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)


        try:
            # 上传文件到OSS
            bucket.put_object_from_file(result_path, result_path)
            object_url = bucket.sign_url('GET', result_path, 600)
            self.write_success_data(object_url)
        except oss2.exceptions.OssError as e:
            print("error")

