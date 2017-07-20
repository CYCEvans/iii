package com.xxx.HW;

public class Hw01_2 {
	public static void main(String[] args){
		//請設計一隻Java程式，計算1～1000的偶數和 (2+4+6+8+…+1000)
		int even =0;
		for (int i=1;i<=1000;i++){
			if (i%2 ==0){
				even +=i;
			}
			else{continue;}
		}
		System.out.printf("偶數和為%d%n", even);
		//請設計一隻Java程式，計算1～10的連乘積 (1*2*3*…*10) (用for迴圈)
		int product =1;
		for(int i =1;i<=10;i++){
			product *=i;
		}
		System.out.printf("1到10連乘積為%d%n", product);
		//請設計一隻Java程式，計算1～10的連乘積 (1*2*3*…*10) (用while迴圈)
		int product2 =1;
		int count =1;
		while(count<=10){
			product2 *=count;
			count +=1;
		}
		System.out.printf("1到10連乘積為%d%n", product2);
		//請設計一隻Java程式，輸出結果為以下：1、4、9、16、25、36、49、64、81、100
		for(int i =1; i<=10;i++){
			System.out.printf("%d ",(int)(Math.pow(i,2)));	
		}
		System.out.println();
		/*阿文很熱衷大樂透 (1 ～ 49)，但他不喜歡有4的數字，不論是個位數或是十位數。
	            請設計一隻程式，輸出結果為阿文可以選擇的數字有哪些？總共有幾個？*/
		int sum =0;
		for (int n =1;n<=49;n++){
			if(n/10 != 4 && n%10 !=4){
				sum +=1;
				System.out.printf("%d ",n);
			}	
		}
		System.out.printf("總共有%d個%n",sum);
		/*請設計一隻Java程式，輸出結果為以下：
		1 2 3 4 5 6 7 8 9 10
		1 2 3 4 5 6 7 8 9
		1 2 3 4 5 6 7 8
		1 2 3 4 5 6 7
		1 2 3 4 5 6
		1 2 3 4 5
		1 2 3 4
		1 2 3
		1 2
		1*/
		for(int i=10; i>=1;i-- ){
			for(int j = 1;j <=i;j++){	
				System.out.printf("%d ",j);
			}
			System.out.println();
		}
		/* 請設計一隻Java程式，輸出結果為以下：
		A
		BB
		CCC
		DDDD
		EEEEE
		FFFFFF*/
		for(int i=1,k=65; i<=5;i++,k++){ //65=0041 'A'的unicode代碼
			for(int j = 1;j <=i;j++){	
				System.out.printf("%c", k);
			}
			System.out.println();
		}
//		for (int n1 = 1,n2=65; n1 <= 5; n1++,n2++) { 
//			char n = (char)n2;
//			for (int n3= 1; n3 <= n1; n3++) {
//				System.out.print(n);
//				}
//			System.out.println();
//		}
	}

}
