@profile
def main():
	array = []
	for i in range(9):
	    array.append(int(input()))
	
	array.sort()
	
	sum_ = sum(array)
	
	# 만약 모두다 더하고 2명을 뺐을 때 그 값이 100이라면 2개를 뺀 나머지 값들 출력
	for i in range(len(array)):
	    for j in range(i + 1, len(array)):
	        if sum_ - array[i] - array[j] == 100:
	            for k in range(len(array)):
	                if k == i or k == j:
	                    pass
	                else:
	                    print(array[k])
	            exit()
main()