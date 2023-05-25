@profile
def main():
	s = input()
	n = len(s)
	
	# 길이 1인 부분수열은 모두 팰린드롬
	count = n
	
	# 길이 2 이상인 부분수열에 대해 팰린드롬 개수 계산
	for length in range(2, n + 1):
	    for i in range(n - length + 1):
	        j = i + length - 1
	
	        # 양 끝 문자가 같을 경우, 양 끝 문자를 포함한 부분수열은 새로운 팰린드롬 개수를 추가함
	        if s[i] == s[j]:
	            count += 1
	
	print(count)
main()