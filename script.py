from functions import functions as f

path = 'input/test'
extension_in = ['tif', 'jpg']
extension_out = 'png'
parent_suffix = '../../output/converted/'
file_suffix = 'out'
iter_timer = 1

if __name__ == "__main__":
    # entry point to the convert_image_directory function
    f.convert_image_directory(path,
                              extension_in=extension_in,
                              extension_out=extension_out,
                              file_suffix=file_suffix,
                              parent_suffix=parent_suffix,
                              iter_timer=iter_timer)
