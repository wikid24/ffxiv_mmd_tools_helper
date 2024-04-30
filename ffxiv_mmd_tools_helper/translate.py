import bpy

jp_half_to_full = (
    ('ｳﾞ', 'ヴ'), ('ｶﾞ', 'ガ'), ('ｷﾞ', 'ギ'), ('ｸﾞ', 'グ'), ('ｹﾞ', 'ゲ'),
    ('ｺﾞ', 'ゴ'), ('ｻﾞ', 'ザ'), ('ｼﾞ', 'ジ'), ('ｽﾞ', 'ズ'), ('ｾﾞ', 'ゼ'),
    ('ｿﾞ', 'ゾ'), ('ﾀﾞ', 'ダ'), ('ﾁﾞ', 'ヂ'), ('ﾂﾞ', 'ヅ'), ('ﾃﾞ', 'デ'),
    ('ﾄﾞ', 'ド'), ('ﾊﾞ', 'バ'), ('ﾊﾟ', 'パ'), ('ﾋﾞ', 'ビ'), ('ﾋﾟ', 'ピ'),
    ('ﾌﾞ', 'ブ'), ('ﾌﾟ', 'プ'), ('ﾍﾞ', 'ベ'), ('ﾍﾟ', 'ペ'), ('ﾎﾞ', 'ボ'),
    ('ﾎﾟ', 'ポ'), ('｡', '。'), ('｢', '「'), ('｣', '」'), ('､', '、'),
    ('･', '・'), ('ｦ', 'ヲ'), ('ｧ', 'ァ'), ('ｨ', 'ィ'), ('ｩ', 'ゥ'),
    ('ｪ', 'ェ'), ('ｫ', 'ォ'), ('ｬ', 'ャ'), ('ｭ', 'ュ'), ('ｮ', 'ョ'),
    ('ｯ', 'ッ'), ('ｰ', 'ー'), ('ｱ', 'ア'), ('ｲ', 'イ'), ('ｳ', 'ウ'),
    ('ｴ', 'エ'), ('ｵ', 'オ'), ('ｶ', 'カ'), ('ｷ', 'キ'), ('ｸ', 'ク'),
    ('ｹ', 'ケ'), ('ｺ', 'コ'), ('ｻ', 'サ'), ('ｼ', 'シ'), ('ｽ', 'ス'),
    ('ｾ', 'セ'), ('ｿ', 'ソ'), ('ﾀ', 'タ'), ('ﾁ', 'チ'), ('ﾂ', 'ツ'),
    ('ﾃ', 'テ'), ('ﾄ', 'ト'), ('ﾅ', 'ナ'), ('ﾆ', 'ニ'), ('ﾇ', 'ヌ'),
    ('ﾈ', 'ネ'), ('ﾉ', 'ノ'), ('ﾊ', 'ハ'), ('ﾋ', 'ヒ'), ('ﾌ', 'フ'),
    ('ﾍ', 'ヘ'), ('ﾎ', 'ホ'), ('ﾏ', 'マ'), ('ﾐ', 'ミ'), ('ﾑ', 'ム'),
    ('ﾒ', 'メ'), ('ﾓ', 'モ'), ('ﾔ', 'ヤ'), ('ﾕ', 'ユ'), ('ﾖ', 'ヨ'),
    ('ﾗ', 'ラ'), ('ﾘ', 'リ'), ('ﾙ', 'ル'), ('ﾚ', 'レ'), ('ﾛ', 'ロ'),
    ('ﾜ', 'ワ'), ('ﾝ', 'ン'),
    )

jp_uni_to_ascii=(
# full-width unicode forms I think: https://en.wikipedia.org/wiki/Halfwidth_and_fullwidth_forms
('０', '0'), ('１', '1'), ('２', '2'), ('３', '3'), ('４', '4'), ('５', '5'), ('６', '6'), ('７', '7'), ('８', '8'), ('９', '9'),
('ａ', 'a'), ('ｂ', 'b'), ('ｃ', 'c'), ('ｄ', 'd'), ('ｅ', 'e'), ('ｆ', 'f'), ('ｇ', 'g'), ('ｈ', 'h'), ('ｉ', 'i'), ('ｊ', 'j'),
('ｋ', 'k'), ('ｌ', 'l'), ('ｍ', 'm'), ('ｎ', 'n'), ('ｏ', 'o'), ('ｐ', 'p'), ('ｑ', 'q'), ('ｒ', 'r'), ('ｓ', 's'), ('ｔ', 't'), 
('ｕ', 'u'), ('ｖ', 'v'), ('ｗ', 'w'), ('ｘ', 'x'), ('ｙ', 'y'), ('ｚ', 'z'),
('Ａ', 'A'), ('Ｂ', 'B'), ('Ｃ', 'C'), ('Ｄ', 'D'), ('Ｅ', 'E'), ('Ｆ', 'F'), ('Ｇ', 'G'), ('Ｈ', 'H'), ('Ｉ', 'I'), ('Ｊ', 'J'),
('Ｋ', 'K'), ('Ｌ', 'L'), ('Ｍ', 'M'), ('Ｎ', 'N'), ('Ｏ', 'O'), ('Ｐ', 'P'), ('Ｑ', 'Q'), ('Ｒ', 'R'), ('Ｓ', 'S'), ('Ｔ', 'T'), 
('Ｕ', 'U'), ('Ｖ', 'V'), ('Ｗ', 'W'), ('Ｘ', 'X'), ('Ｙ', 'Y'), ('Ｚ', 'Z'),
('＋', '+'), ('－', '-'), ('＿', '_'), ('／', '/'),
)

def parseJp(input_string):
    # Initialize the output string
    output_string = input_string

    # Iterate over each list of replacement tuples
    for item in jp_half_to_full:
        output_string = output_string.replace(item[0], item[1])

    for item in jp_uni_to_ascii:
        output_string = output_string.replace(item[0], item[1])

    return output_string




"""
jp_to_en_tuples = [
  ('全ての親', 'ParentNode'),
  ('操作中心', 'ControlNode'),               
  ('センター', 'Center'),
  ('ｾﾝﾀｰ', 'Center'),
  ('グループ', 'Group'),
  ('グルーブ', 'Groove'),
  ('キャンセル', 'Cancel'),
  ('上半身', 'UpperBody'),
  ('下半身', 'LowerBody'),
  ('手首', 'Wrist'),
  ('足首', 'Ankle'),
  ('首', 'Neck'),
  ('頭', 'Head'),
  ('顔', 'Face'),
  ('下顎', 'Chin'),
  ('下あご', 'Chin'),
  ('あご', 'Jaw'),
  ('顎', 'Jaw'),
  ('両目', 'Eyes'),
  ('目', 'Eye'),
  ('眉', 'Eyebrow'),
  ('舌', 'Tongue'),
  ('涙', 'Tears'),
  ('泣き', 'Cry'),
  ('歯', 'Teeth'),
  ('照れ', 'Blush'),
  ('青ざめ', 'Pale'),
  ('ガーン', 'Gloom'),
  ('汗', 'Sweat'),
  ('怒', 'Anger'),
  ('感情', 'Emotion'),
  ('符', 'Marks'),
  ('暗い', 'Dark'),
  ('腰', 'Waist'),
  ('髪', 'Hair'),  
  ('三つ編み', 'Braid'),
  ('胸', 'Breast'),
  ('乳', 'Boob'),
  ('おっぱい', 'Tits'),
  ('筋', 'Muscle'),
  ('腹', 'Belly'),
  ('鎖骨', 'Clavicle'),
  ('肩', 'Shoulder'),
  ('腕', 'Arm'),
  ('うで', 'Arm'),
  ('ひじ', 'Elbow'),
  ('肘', 'Elbow'),
  ('手', 'Hand'),
  ('親指', 'Thumb'),
  ('人指', 'IndexFinger'),
  ('人差指', 'IndexFinger'),
  ('中指', 'MiddleFinger'),
  ('薬指', 'RingFinger'),
  ('小指', 'LittleFinger'),  
  ('足', 'Leg'),
  ('ひざ', 'Knee'),  
  ('つま', 'Toe'),
  ('袖', 'Sleeve'),
  ('新規', 'New'),
  ('ボーン', 'Bone'),
  ('捩', 'Twist'),
  ('回転', 'Rotation'),
  ('軸', 'Axis'),
  ('ﾈｸﾀｲ', 'Necktie'),
  ('ネクタイ', 'Necktie'),
  ('ヘッドセット', 'Headset'),
  ('飾り', 'Accessory'),
  ('リボン', 'Ribbon'),
  ('襟', 'Collar'),
  ('紐', 'String'),
  ('コード', 'Cord'),
  ('イヤリング', 'Earring'),
  ('メガネ', 'Eyeglasses'),
  ('眼鏡', 'Glasses'),
  ('帽子', 'Hat'),
  ('ｽｶｰﾄ', 'Skirt'),
  ('スカート', 'Skirt'),
  ('パンツ', 'Pantsu'),
  ('シャツ', 'Shirt'),
  ('フリル', 'Frill'),
  ('マフラー', 'Muffler'),
  ('ﾏﾌﾗｰ', 'Muffler'),
  ('服', 'Clothes'),
  ('ブーツ', 'Boots'),
  ('ねこみみ', 'CatEars'),
  ('ジップ', 'Zip'),
  ('ｼﾞｯﾌﾟ', 'Zip'),
  ('ダミー', 'Dummy'),
  ('ﾀﾞﾐｰ', 'Dummy'),
  ('基', 'Category'),
  ('あほ毛', 'Antenna'),
  ('アホ毛', 'Antenna'),
  ('モミアゲ', 'Sideburn'),
  ('もみあげ', 'Sideburn'),
  ('ツインテ', 'Twintail'),
  ('おさげ', 'Pigtail'),
  ('ひらひら', 'Flutter'),
  ('調整', 'Adjustment'),
  ('補助', 'Aux'),
  ('右', 'Right'),
  ('左', 'Left'),  
  ('前', 'Front'),
  ('後ろ', 'Behind'),
  ('後', 'Back'),
  ('横', 'Side'),
  ('中', 'Middle'),
  ('上', 'Upper'),
  ('下', 'Lower'),
  ('親', 'Parent'),  
  ('先', 'Tip'),
  ('パーツ', 'Part'),
  ('光', 'Light'),
  ('戻', 'Return'),
  ('羽', 'Wing'),
  ('根', 'Base'), # ideally 'Root' but to avoid confusion
  ('毛', 'Strand'),
  ('尾', 'Tail'),
  ('尻', 'Butt'),

  ('.', '_'), # probably should be combined with the global 'use underscore' option
 ]




def translateFromJp(name):
    for tuple in jp_to_en_tuples:
        if tuple[0] in name:
            name = name.replace(tuple[0], tuple[1])
    return name


def half_to_full(self, name):
    return self.replace_from_tuples(name, jp_half_to_full_tuples)

def is_translated(self, name):
    try:
        name.encode('ascii', errors='strict')
    except UnicodeEncodeError:
        return False
    return True

def translate(self, name, default=None, from_full_width=True):
    if from_full_width:
        name = self.half_to_full(name)
    name_new = self.replace_from_tuples(name, self.__csv_tuples)
    if default is not None and not self.is_translated(name_new):
        self.__fails[name] = name_new
        return default
    return name_new

"""