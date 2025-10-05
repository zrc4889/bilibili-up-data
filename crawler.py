import os
from bilibili_api import user, sync
import json

# 配置：替换为你要跟踪的UP主的MID
UP_MID = int(os.environ.get('UP_MID', 'YOUR_UP_MID'))  # 示例：12345678

async def main():
    u = user.User(UP_MID)
    
    # 获取UP主基本信息
    user_info = await u.get_user_info()
    # 获取UP主视频列表（例如前20个）
    videos = await u.get_videos(ps=20)
    # 获取UP主动态（例如前20条）
    dynamics = await u.get_dynamics(offset=0, need_top=False)

    # 整理需要的数据
    data = {
        'user_info': {
            'name': user_info['name'],
            'mid': user_info['mid'],
            'face': user_info['face'],
            'follower': user_info['follower']
        },
        'videos': [],
        'dynamics': []
    }

    # 处理视频列表
    for video in videos['list']['vlist']:
        data['videos'].append({
            'title': video['title'],
            'bvid': video['bvid'],
            'description': video['description'],
            'created': video['created'],
            'length': video['length'],
            'play': video['play']
        })

    # 处理动态列表（简化示例，实际结构更复杂）
    if 'cards' in dynamics:
        for card in dynamics['cards']:
            # 这里是基础提取，你可以根据需要添加更多字段
            data['dynamics'].append({
                'dynamic_id': card['desc']['dynamic_id'],
                'timestamp': card['desc']['timestamp'],
                'type': card['desc']['type']
            })

    return data

if __name__ == '__main__':
    data = sync(main())
    # 将数据保存到JSON文件
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('数据获取完成，已保存到 data.json')
