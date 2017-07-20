package com.xxx.HW;

public class Hw01_1 {
	public static void main(String[] args){
		//請設計一隻Java程式，計算12，6這兩個數值的和與積
		int n=6,m=12;
		System.out.printf("%d與%d的和為%2d，積為%2d%n", n,m,n+m,n*m);
		//請設計一隻Java程式，計算200顆蛋共是幾打幾顆？ (一打為12顆)
		int eggs=200,dozen=12;
		System.out.printf("%d顆雞蛋是%d打%2d顆%n", eggs,eggs/dozen,eggs%dozen);
		//請由程式算出256559秒為多少天、多少小時、多少分與多少秒
		int num=256559,sec=1,min=sec*60,hour=min*60,day=hour*24;
		System.out.printf("%d秒是%d天%d時%d分%d秒%n", num,num/day,
				(num%day)/hour,
				((num%day)%hour)/min,
				(((num%day)%hour)%min)/sec);
		//請定義一個常數為3.1415(圓周率)，並計算半徑為5的圓面積與圓周長
		final double PI= 3.1415;
		int r =5;
		System.out.printf("半徑%d的圓面積為%.4f圓周長為%.4f%n",r,PI*Math.pow(r,2),2*PI*r);
		//某人在銀行存入150萬，銀行利率為2%，如果每年利息都繼續存入銀行，請用程式計算10年後，本金加利息共有多少錢
		int money =1_500_000;
		double rate = 1.02;
		System.out.printf("10年後本金共%f%n",money*Math.pow(rate,10));
		//請寫一隻程式，利用System.out.println()印出以下三個運算式結果：
		System.out.println(5+5);//兩個int相加為10(純數相加)
		System.out.println(5+'5');//char自動轉換成unicode代碼為35(16進位)，轉換成10進位為53，相加為58
		System.out.println(5+"5");//int和字串相加產生新字串，5直接加入第一個5後面(視同兩個字串相加)
	
	
	}

}
