import tornado.ioloop
import tornado.web
import handler.upload as upload
import os
import qiconfig.qiconfig as config

def make_app():
    config_path = config.get_config('file_path')
    root_folder = config_path['root_folder']
    static_folder = config_path['static']
    static_path = os.path.join(root_folder, static_folder)
    return tornado.web.Application([
        (r"/upload",    upload.UploadHandler)
    ])


if __name__ == "__main__":
    app = make_app()
    port = 9000
    print('app service listen %d' % port)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
