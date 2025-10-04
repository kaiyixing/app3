from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# 存储接收到的招聘信息（使用全局变量，简单但注意：多实例部署会有数据不一致问题）
job_listings = []

@app.route('/')
def index():
    """主页，显示招聘信息列表"""
    html_template = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>招聘信息展示</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }
        .container { max-width: 1200px; margin: 0 auto; }
        header { background: #007bff; color: white; padding: 1rem; text-align: center; border-radius: 8px; }
        .job-card { background: white; padding: 20px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .refresh-btn { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 20px 0; }
        .no-jobs { text-align: center; padding: 40px; background: white; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <header><h1>招聘信息展示平台</h1></header>
        <button class="refresh-btn" onclick="location.reload()">刷新列表</button>
        <div id="jobs">
            {% if jobs %}
                {% for job in jobs %}
                <div class="job-card">
                    <h3>{{ job.username or '未命名职位' }}</h3>
                    <p>{{ job.avatar_text or '无描述' }}</p>
                </div>
                {% endfor %}
            {% else %}
                <div class="no-jobs">暂无招聘信息</div>
            {% endif %}
        </div>
    </div>
</body>
</html>
    '''
    return render_template_string(html_template, jobs=job_listings)

@app.route('/post-job', methods=['POST'])
def handle_post_job():
    """处理招聘信息提交"""
    # 解析表单数据
    username = request.form.get('username', '未命名')
    avatar_text = request.form.get('avatar', '无描述')
    
    # 添加到列表
    job_listings.append({
        "username": username,
        "avatar_text": avatar_text
    })
    
    return jsonify({
        "status": "success",
        "message": "提交成功"
    })

if __name__ == '__main__':
    # 从环境变量获取端口（兼容部署平台的动态端口）
    port = int(os.environ.get('PORT', 5000))
    # 生产环境禁用debug，绑定所有地址
    app.run(host='0.0.0.0', port=port, debug=False)
