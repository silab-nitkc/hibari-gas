# 難読化対象の命令（ジャンプ命令は現時点で設定不可）
TARGET_OP = [
    'add',
    'sub',
    'xor',
    'and',
    'or' ,
]
# 入出力例の個数
IOExample_N = 3
# 入出力テスト時の試行回数
TEST_N  = 1000
# 命令列生成の再試行回数（上限）
RETRY_MAX = 3