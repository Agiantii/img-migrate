import re
import requests
import os

include_message = "xxx"
exclude_message = ""

encoding_way = "utf-8"

origin_workbench = r"D:\test\img-migrate\notebook-origin"
target_workbench = r"D:\test\img-migrate\agiantii-note-book"
if (os.path.exists(target_workbench) == False):
    os.mkdir(target_workbench)
target_imgs_path_basename = "imgs"
target_imgs_dir = os.path.join(target_workbench, target_imgs_path_basename)
if (os.path.exists(target_imgs_dir) == False):
    os.mkdir(target_imgs_dir)


def download_img(img_url, target_dir):
    # 直接取得 url 的最后一部分作为文件名
    img_name = img_url.split('/')[-1]
    if(os.path.exists(os.path.join(target_dir, img_name))) :
        print(f'{img_name} already exists.')
        return  
    # print(f'Downloading {img_name}...')
    img_content = requests.get(img_url).content
    with open(os.path.join(target_imgs_dir, img_name), 'wb') as f:
        f.write(img_content)
    print(f'{img_name} downloaded.')


def download_imgs(img_lis):
    for img_url in img_lis:
        download_img(img_url, target_imgs_dir)


def replace_img_urls(file_path: str, new_md_path: str, dep: int = 0) -> None:
    '''
    替换 目标 md 文件中的 图片链接
    并写到 新的 md 文件中
    '''
    # 取得 file_path md 的 文件名
    def replace_with_path(match):
        # 提取文件名
        filename = match.group(1).split('/')[-1]
        # 返回新的路径和文件名
        new_path = f"{'../'* dep}{target_imgs_path_basename}/{filename}"
        res = f"![]({new_path})"
        print(res)
        return res
        # return f"![]({new_path})"
    file_name = os.path.basename(file_path)
    print(f'new_md_path:{os.path.abspath(new_md_path)}')
    with open(file_path, 'r',encoding=encoding_way) as f:
        content = f.read()
        pattern = re.compile(f'!\[.*?\]\(.*?{include_message}.*?/(.*?)\)')
        new_content = re.sub(pattern, replace_with_path, content)
        # print(re.findall(pattern,content))
    with open(new_md_path, 'w',encoding=encoding_way) as f:
        f.write(new_content)


def deal_with_file(file_path: str, dep: int = 1):
    if (file_path.endswith('.md') != True):
        return
    file_base_name = os.path.basename(file_path)
    with open(file_path, 'r', encoding=encoding_way) as f:
        content = f.read()
        pattern = re.compile(f'!\[.*?\]\((.*?{include_message}.*?)\)')
        origin_img_urls = pattern.findall(content)
        print(f'origin_img_urls:{origin_img_urls}')
        download_imgs(origin_img_urls)
        rel_path = os.path.relpath(file_path, origin_workbench)
        print(rel_path)
        replace_img_urls(file_path, os.path.join(
            target_workbench, rel_path), dep)


def deal_with_dir(work_dir, dep=1):
    rel_name = os.path.relpath(work_dir, origin_workbench)
    temp_dir = os.path.join(target_workbench, rel_name)
    if (not os.path.exists(temp_dir)):
        os.makedirs(temp_dir)
    print(temp_dir)
    for i in os.listdir(work_dir):
        if os.path.isdir(os.path.join(work_dir, i)):
            deal_with_dir(os.path.join(work_dir, i), dep+1)
        else:
            deal_with_file(os.path.join(work_dir, i),dep)
if __name__ == '__main__':
    deal_with_dir(origin_workbench, dep=0)