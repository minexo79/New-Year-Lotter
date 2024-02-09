from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_admin import Admin, expose, BaseView
import random 
from gconfig import GConfig
from globalvar import lotteryResult

app = Flask(__name__)
admin = Admin(app, name="新年紅包後台", template_mode='bootstrap4')

clicks = {} 
win_count = 0

local_config = {
    'redEnvCount': int,
    'minClick': int,
    'maxClick': int
}

def update_local_config(_redEnvCount: int,
                        _minClick: int,
                        _maxClick: int):
    local_config['redEnvCount'] = _redEnvCount
    local_config['minClick'] = _minClick
    local_config['maxClick'] = _maxClick


class LotteryConfig(BaseView):
    @expose('/') # 用法等於路由
    def index(self):
        return self.render('admin/lotteryconfig.html', 
                            redEnvCount = config.redEnvCount, 
                            minClick = config.minClick, 
                            maxClick = config.maxClick)

    @expose('/save_config', methods=['POST'])
    def save_config(self):
        config.redEnvCount = request.form['redEnvCount']
        config.minClick = request.form['minClick']
        config.maxClick = request.form['maxClick']
        config.write()

        update_local_config(config.redEnvCount, 
                            config.minClick, 
                            config.maxClick)

        return redirect(url_for('index'))

@app.route('/')
def index():
    global win_count
    device_id = request.remote_addr

    # 限制紅包抽獎數量
    if (win_count >= local_config['redEnvCount']):
        return render_template('index.html', ip = request.remote_addr, count = win_count, message = '紅包已抽完，明年再來吧!')

    if device_id in clicks:
        device = clicks[device_id]
        if device[1] == lotteryResult.Win:
            return render_template('index.html', ip = request.remote_addr, count = win_count, message = '恭喜得獎!')
        elif device[1] == lotteryResult.Lose:
            return render_template('index.html', ip = request.remote_addr, count = win_count, message = '請連續點擊下方紅包')
    
    return render_template('index.html', ip = request.remote_addr, count = win_count, message = '請連續點擊下方紅包')

@app.route('/click', methods=['POST']) 
def click():
    global win_count
    device_id = request.remote_addr

    # 初始化記錄點擊次數
    if device_id not in clicks:
        clicks[device_id] = [0, lotteryResult.none]

    # 限制每個IP只能抽一次
    # 2024.2.9 Blackcat: 改成不限制抽獎次數，若發現為lose則清除紀錄
    if clicks[device_id][1] == lotteryResult.Win:
        return jsonify({'message': '你已得獎，請勿重複嘗試!'})
    else:
        clicks[device_id][0] += 1

    app.logger.debug('%s clicked the button %s times!', request.remote_addr, clicks[device_id][0])

    # 50~100次隨機抽獎
    if clicks[device_id][0] >= random.randint(local_config['minClick'], local_config['maxClick']):
        prize = random.choice(['恭喜得獎!', '沒抽到紅包，再試一下!'])
        # 限制最多3個獎項
        if prize == '恭喜得獎!' and win_count < local_config['redEnvCount']:
            app.logger.info('%s win the lottery!', request.remote_addr)
            # 記錄中獎
            clicks[device_id][1] = lotteryResult.Win
            win_count += 1
        else:
            app.logger.info('%s lose the lottery', request.remote_addr)
            clicks[device_id][0] = 1
            clicks[device_id][1] = lotteryResult.none
        
        return jsonify({'message': prize})

    return jsonify({'message': ''})

if __name__ == '__main__':
    # read config file
    config = GConfig("config.ini")
    config.read()

    update_local_config(config.redEnvCount, 
                        config.minClick, 
                        config.maxClick)

    admin.add_view(LotteryConfig(name='設定'))

    app.logger.setLevel(10)
    app.run(host='0.0.0.0', port=9004, debug=False)