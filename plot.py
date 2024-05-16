import matplotlib.pyplot as plt
import re

scores = []
#yang_wxyy_
scores = [('test16', 1.0), ('test151', 1.0), ('test29', 1.0), ('test11', 1.0), ('test156', 1.0), ('test27', 1.0), ('test18', 1.0), ('test160', 1.0), ('test158', 0.26798995532104675), ('test20', 1.0), ('test133', 0.3991735270428161), ('test80', 1.0), ('test74', 0.2888249699575745), ('test134', 0.3248560603425911), ('test73', 1.0), ('test87', 1.0), ('test102', 1.0), ('test45', 1.0), ('test89', 1.0), ('test105', 1.0), ('test42', 1.0), ('test21', 1.0), ('test159', 0.2501918044061379), ('test26', 1.0), ('test161', 1.0), ('test19', 1.0), ('test10', 1.0), ('test157', 1.0), ('test17', 1.0), ('test28', 1.0), ('test150', 1.0), ('test88', 1.0), ('test104', 1.0), ('test43', 1.0), ('test103', 1.0), ('test44', 1.0), ('test135', 1.0), ('test86', 0.318786934878612), ('test72', 1.0), ('test132', 1.0), ('test75', 0.1853289717722033), ('test81', 1.0), ('test9', 1.0), ('test7', 1.0), ('test6', 1.0), ('test1', 0.14219755438219234), ('test8', 0.38200717610914836), ('test57', 1.0), ('test68', 1.0), ('test110', 1.0), ('test128', 0.27294030930023455), ('test50', 1.0), ('test117', 1.0), ('test92', 0.24982675150100284), ('test66', 1.0), ('test121', 0.25791895843125584), ('test59', 1.0), ('test61', 1.0), ('test95', 1.0), ('test119', 0.24080063557717055), ('test126', 0.3845093267267579), ('test35', 1.0), ('test32', 1.0), ('test143', 1.0), ('test144', 0.17532562829531678), ('test94', 0.1978525518024853), ('test118', 1.0), ('test60', 1.0), ('test127', 1.0), ('test67', 1.0), ('test93', 1.0), ('test58', 0.21380434378854055), ('test120', 0.2014155296835196), ('test51', 1.0), ('test129', 0.20522159076260962), ('test116', 1.0), ('test56', 1.0), ('test111', 1.0), ('test69', 1.0), ('test145', 1.0), ('test142', 1.0), ('test33', 1.0), ('test34', 0.2901806160097148), ('test137', 1.0), ('test70', 1.0), ('test108', 1.0), ('test84', 1.0), ('test130', 1.0), ('test48', 1.0), ('test83', 1.0), ('test77', 1.0), ('test106', 0.5191589387842942), ('test139', 1.0), ('test41', 0.42059769566958694), ('test79', 1.0), ('test101', 1.0), ('test46', 0.1891961003004509), ('test12', 1.0), ('test155', 1.0), ('test15', 1.0), ('test152', 1.0), ('test23', 1.0), ('test24', 1.0), ('test100', 0.17393507521608906), ('test78', 1.0), ('test47', 1.0), ('test107', 0.2439098980778362), ('test40', 0.4071727610598148), ('test138', 1.0), ('test49', 1.0), ('test131', 0.3240564047763323), ('test76', 1.0), ('test82', 0.2944970551714756), ('test136', 1.0), ('test109', 0.3026978842695211), ('test85', 1.0), ('test71', 1.0), ('test25', 1.0), ('test162', 0.21201033098333502), ('test22', 1.0), ('test14', 1.0), ('test153', 1.0), ('test13', 1.0), ('test154', 1.0), ('test4', 1.0), ('test3', 1.0), ('test2', 0.7304315402341571), ('test5', 1.0), ('test149', 1.0), ('test31', 1.0), ('test36', 1.0), ('test147', 1.0), ('test140', 0.35963209910258076), ('test38', 1.0), ('test53', 0.5900167501688374), ('test114', 1.0), ('test98', 0.24637638300553524), ('test54', 0.41399463402430364), ('test113', 1.0), ('test62', 1.0), ('test96', 1.0), ('test125', 0.2569409604290972), ('test91', 1.0), ('test65', 1.0), ('test122', 1.0), ('test39', 1.0), ('test141', 1.0), ('test146', 0.20736590130930654), ('test37', 1.0), ('test30', 1.0), ('test148', 1.0), ('test64', 1.0), ('test90', 1.0), ('test123', 1.0), ('test97', 1.0), ('test63', 0.25931442722706366), ('test124', 0.43714178875638005), ('test55', 0.11067755533951328), ('test112', 1.0), ('test52', 1.0), ('test115', 1.0), ('test99', 0.287410082834154)]

#li_zhipu_scores  = [('test1', 1), ('test10', 1.0), ('test100', 0.15482839479145732), ('test101', 1.0), ('test102', 1.0), ('test103', 1.0), ('test104', 1.0), ('test105', 1.0), ('test106', 0.5491355015642931), ('test107', 0.2561211649311788), ('test108', 1.0), ('test109', 0.3140732011566847), ('test11', 1.0), ('test110', 0.22965869982401932), ('test111', 1.0), ('test112', 0.4085830104793767), ('test113', 1.0), ('test114', 0.44839924671191345), ('test115', 1.0), ('test116', 1.0), ('test117', 0.4077677730176097), ('test118', 1.0), ('test119', 0.2404964271634326), ('test12', 1.0), ('test120', 0.20184704564086303), ('test121', 1.0), ('test122', 1.0), ('test123', 1.0), ('test124', 0.3877268433542055), ('test125', 0.24723442406289092), ('test126', 0.3619609930580307), ('test127', 1.0), ('test128', 1.0), ('test129', 0.2283064236094128), ('test13', 1.0), ('test130', 1.0), ('test131', 0.28656916921699566), ('test132', 1.0), ('test133', 0.31435444906512505), ('test134', 0.36874363124000503), ('test135', 1.0), ('test136', 1.0), ('test137', 1.0), ('test138', 1.0), ('test139', 1.0), ('test14', 1.0), ('test140', 1.0), ('test141', 1.0), ('test142', 1.0), ('test143', 1.0), ('test144', 0.2187600716720861), ('test145', 1.0), ('test146', 0.4439220336918764), ('test147', 1.0), ('test148', 0.2842180775509208), ('test149', 1.0), ('test15', 1.0), ('test150', 1.0), ('test151', 1.0), ('test152', 1.0), ('test153', 1.0), ('test154', 1.0), ('test155', 1.0), ('test156', 1.0), ('test157', 1.0), ('test158', 1.0), ('test159', 0.24873484206453875), ('test16', 1.0), ('test160', 1.0), ('test161', 1.0), ('test162', 0.20515116758104712), ('test17', 1.0), ('test18', 1.0), ('test19', 1.0), ('test2', 0.8011254178514978), ('test20', 1.0), ('test21', 1.0), ('test22', 1.0), ('test23', 1.0), ('test24', 1.0), ('test25', 1.0), ('test26', 1.0), ('test27', 1.0), ('test28', 0.5621451039174736), ('test29', 1.0), ('test3', 1.0), ('test30', 1.0), ('test31', 1.0), ('test32', 1.0), ('test33', 1.0), ('test34', 0.29050208687560786), ('test35', 1.0), ('test36', 1.0), ('test37', 1.0), ('test38', 1.0), ('test39', 1.0), ('test4', 0.49401030142247754), ('test40', 1.0), ('test41', 1.0), ('test42', 1.0), ('test43', 1.0), ('test44', 1.0), ('test45', 1.0), ('test46', 1.0), ('test47', 1.0), ('test48', 1.0), ('test49', 1.0), ('test5', 1.0), ('test50', 1.0), ('test51', 1.0), ('test52', 1.0), ('test53', 0.6141593851649939), ('test54', 0.38242546438653957), ('test55', 1.0), ('test56', 1.0), ('test57', 1.0), ('test58', 1.0), ('test59', 1.0), ('test6', 1.0), ('test60', 1.0), ('test61', 1.0), ('test62', 1.0), ('test63', 1.0), ('test64', 1.0), ('test65', 1.0), ('test66', 1.0), ('test67', 1.0), ('test68', 1.0), ('test69', 1.0), ('test7', 1.0), ('test70', 1.0), ('test71', 1.0), ('test72', 1.0), ('test73', 1.0), ('test74', 0.3319510718071842), ('test75', 1.0), ('test76', 1.0), ('test77', 1.0), ('test78', 1.0), ('test79', 0.2781147098671371), ('test8', 0.48971172413407993), ('test80', 1.0), ('test81', 1.0), ('test82', 0.38047875746611026), ('test83', 1.0), ('test84', 1.0), ('test85', 1.0), ('test86', 1.0), ('test87', 1.0), ('test88', 1.0), ('test89', 1.0), ('test9', 1.0), ('test90', 1.0), ('test91', 1.0), ('test92', 0.3069459961034415), ('test93', 1.0), ('test94', 0.19997973300735813), ('test95', 1.0), ('test96', 1.0), ('test97', 1.0), ('test98', 1.0), ('test99', 1.0)]

#yang_gpt4_scores = [('test16', 1.0), ('test151', 1.0), ('test29', 1.0), ('test11', 1.0), ('test156', 1.0), ('test27', 1.0), ('test18', 1.0), ('test160', 1.0), ('test158', 1.0), ('test20', 1.0), ('test133', 0.2199891573725004), ('test80', 1.0), ('test74', 1.0), ('test134', 1.0), ('test73', 1.0), ('test87', 1.0), ('test102', 1.0), ('test45', 1.0), ('test89', 1.0), ('test105', 0.1356218578827705), ('test42', 1.0), ('test21', 1.0), ('test159', 1.0), ('test26', 1.0), ('test161', 1.0), ('test19', 0.4305798118718234), ('test10', 1.0), ('test157', 1.0), ('test17', 1.0), ('test28', 1.0), ('test150', 1.0), ('test88', 1.0), ('test104', 1.0), ('test43', 1.0), ('test103', 1.0), ('test44', 1.0), ('test135', 1.0), ('test86', 1.0), ('test72', 1.0), ('test132', 1.0), ('test75', 1.0), ('test81', 1.0), ('test9', 1.0), ('test7', 1.0), ('test6', 1.0), ('test1', 1), ('test8', 1.0), ('test57', 1.0), ('test68', 1.0), ('test110', 1.0), ('test128', 0.26435530448145084), ('test50', 1.0), ('test117', 0.4295877151595319), ('test92', 0.3788668654974044), ('test66', 1.0), ('test121', 1.0), ('test59', 1.0), ('test61', 1.0), ('test95', 1.0), ('test119', 1.0), ('test126', 1.0), ('test35', 1.0), ('test32', 1.0), ('test143', 1.0), ('test144', 0.18063686042920366), ('test94', 1.0), ('test118', 1.0), ('test60', 1.0), ('test127', 1.0), ('test67', 1.0), ('test93', 1.0), ('test58', 1.0), ('test120', 0.28406048475838847), ('test51', 1.0), ('test129', 0.4213534473441346), ('test116', 1.0), ('test56', 1.0), ('test111', 1.0), ('test69', 1.0), ('test145', 1.0), ('test142', 1.0), ('test33', 1.0), ('test34', 0.27931153361541516), ('test137', 0.4280435988642496), ('test70', 1.0), ('test108', 1.0), ('test84', 1.0), ('test130', 1.0), ('test48', 1.0), ('test83', 0.3744800407845219), ('test77', 0.24733506475409184), ('test106', 1.0), ('test139', 0.07756401205511564), ('test41', 1.0), ('test79', 1.0), ('test101', 0.5418232557181124), ('test46', 1.0), ('test12', 1.0), ('test155', 1.0), ('test15', 1.0), ('test152', 1.0), ('test23', 1.0), ('test24', 1.0), ('test100', 1.0), ('test78', 1.0), ('test47', 1.0), ('test107', 1.0), ('test40', 1.0), ('test138', 1.0), ('test49', 1.0), ('test131', 0.31354388797075633), ('test76', 1.0), ('test82', 0.4989332898316373), ('test136', 0.3466449433934863), ('test109', 1.0), ('test85', 1.0), ('test71', 1.0), ('test25', 1.0), ('test162', 0.37724725674808274), ('test22', 1.0), ('test14', 1.0), ('test153', 1.0), ('test13', 1.0), ('test154', 1.0), ('test4', 1.0), ('test3', 1.0), ('test2', 1.0), ('test5', 1.0), ('test149', 1.0), ('test31', 1.0), ('test36', 1.0), ('test147', 1.0), ('test140', 1.0), ('test38', 1.0), ('test53', 1.0), ('test114', 0.4713662163618634), ('test98', 1.0), ('test54', 0.5855902774395287), ('test113', 1.0), ('test62', 1.0), ('test96', 1.0), ('test125', 0.23015813336948074), ('test91', 1.0), ('test65', 1.0), ('test122', 1.0), ('test39', 1.0), ('test141', 1.0), ('test146', 0.16432607296757282), ('test37', 1.0), ('test30', 1.0), ('test148', 1.0), ('test64', 1.0), ('test90', 0.27023970053739493), ('test123', 1.0), ('test97', 1.0), ('test63', 1.0), ('test124', 0.3978041028216588), ('test55', 1.0), ('test112', 1.0), ('test52', 1.0), ('test115', 1.0), ('test99', 1.0)]
print(scores[0])

scores = sorted(scores, key=lambda x: int(re.search(r'\d+', x[0]).group()))
print(scores[0],scores[1])
# Extract test names and scores
test_names = [score[0] for score in scores]
test_scores = [score[1] for score in scores]

# Create the bar chart
plt.figure(figsize=(12, 6))
plt.bar(range(len(test_names)), test_scores, width=0.5)
plt.xticks(range(0, len(test_names), 10), test_names[::10], rotation=90)
plt.ylabel('Scores')
plt.title('OpenAI GPT4 2023-07-01-preview Test Scores')    #'Wenxin Yiyan ernie-speed-128k Test Scores') #'Zhipu GLM4 Test Scores') 

# Display the chart
plt.show()