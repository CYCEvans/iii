package com.xxx.HW;


public class HW04_1 {
	
	public static void main(String[] args){
		//有個一維陣列如下：
		//{29, 100, 39, 41, 50, 8, 66, 77, 95, 15}
		//請寫出一隻程式能輸出此陣列所有元素的平均值與大於平均值的元素
		int sum =0;
		int[] ar = {29, 100, 39, 41, 50, 8, 66, 77, 95, 15};
		for(int n=0; n<ar.length;n++ ){
			sum +=ar[n];
		}
		int avg = (sum/ar.length);
		System.out.printf("平均值為%d%n",avg );
		System.out.print("大於平均值為的數有: " );
		for(int n=0; n<ar.length;n++ ){
			if (ar[n]>avg){
				System.out.printf("%d ",ar[n]);
			}
		}
		System.out.println();
//		請建立一個字串，經過程式執行後，輸入結果是反過來的
//		例如String s = “Hello World”，執行結果即為dlroW olleH
		String s = "Hello World"; 
		int leng =s.length()-1;
		for (int n=leng; n>=0 ;n-=1){
			System.out.print(s.charAt(n));
		}
		System.out.println();
		System.out.println("--------------------");
//		有個字串陣列如下(八大行星)：
//		{“mercury”, “venus”, “earth”, “mars”, “jupiter”,“saturn”, “uranus”, “neptune”}
//		請用程式計算出這陣列裡面共有多少個母音(a, e, i, o, u)
		String[] x= {"mercury","venus","earth","mars","jupiter","saturn","uranus","neptune"};
		int totala=0,totale=0,totali=0,totalo=0,totalu=0;
		for (int n=0;n < x.length;n++){
			for (int i=0;i<x[n].length();i++){
				char t = x[n].charAt(i);
				switch (t) {
					case 'a':
						totala +=1;
						break;
					case 'e':
						totale +=1;
						break;
					case 'i':
						totali +=1;
						break;
					case 'o':
						totalo +=1;
						break;
					case 'u':
						totalu +=1;
						break;
				}
			}
		}
		int sum1 =totala+totale+totali+totalo+totalu;
		System.out.printf("a有%d個,e有%d個,i有%d個,o有%d個,u有%d個,共%d個",totala,totale,totali,totalo,totalu,sum1);
		
		
	}
	
}
