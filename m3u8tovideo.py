import os, glob, ffmpeg
from os import mkdir, path, chdir
from shutil import rmtree

def convert_m3u8_to_mp4(m3u8_file_path, dest):
    input_stream = ffmpeg.input(m3u8_file_path)
    output_stream = ffmpeg.output(input_stream, dest, format='mp4')
    ffmpeg.run(output_stream)

def merge_m3u8_contents(index_file_path: str, m3u8_contents_file_path):
    tmp_paths = index_file_path.split('/')
    merged_filename = 'merged_' +  tmp_paths.pop()
    merged_m3u8_file_path = path.join('/'.join(tmp_paths), merged_filename)

    index_file = open(index_file_path, 'r')
    indexes = index_file.read()
    index_file.close()

    output_file = open(merged_m3u8_file_path, 'wb')
    indexes = indexes.split('file:')[1:]
    indexes = [x.split('\n')[0].split('/')[-1] for x in indexes]

    for index in indexes:
        content_file = open(os.path.join(m3u8_contents_file_path, index), 'rb')
        output_file.write(content_file.read())
        content_file.close()

    output_file.close()

    return merged_m3u8_file_path



chdir(root_path)
filenames = [f.split('.')[0] for f in glob.glob("*.m3u8")]
for filename in filenames:
    print('processing ' + filename)
    index_file_path = path.join(root_path, filename) + '.m3u8'
    contents_path = path.join(root_path, filename) + '.m3u8_contents'
    m3u8_file_path = merge_m3u8_contents(index_file_path, contents_path)
    if not os.path.exists(path.join(root_path, 'output')):
        mkdir(path.join(root_path, 'output'))
    mp4_file_path =  path.join(root_path, 'output', filename) + '.mp4'
    convert_m3u8_to_mp4(m3u8_file_path, mp4_file_path)



