package com.xxx.HW;
import java.util.Scanner;
public class HW04_2 {
//	阿文上班時忘了帶錢包,想要向同事借錢,和他交情比較好的同事共有5 個,其員工編號與身上現金列表如下：
//	id		 25 	 32		 8		19		  27
//	money	2500	 800	500	   1000		 1200
//	請設計一個程式,可以讓小華輸入欲借的金額後,便會顯示哪些員工編號的同事
//	有錢可借他;並且統計有錢可借的總人數:例如輸入1000 就顯示「有錢可借的員工編號: 25 19 27 共3 人!」	
	public static void main(String[] args){
		Scanner sc= new Scanner(System.in);
		System.out.println("你想借多少?");
		int mon = sc.nextInt();
		int[][] worker={{25,2500},{32,800},{8,500},{19,1000},{27,1200}};
		int sum =0;
		for(int i=0;i<=worker.length-1;i++){
			if(worker[i][1]>=mon){
				sum+=1;
			}
		}
		System.out.printf( "%s","有錢可借的員工編號: ");
		for(int i=0;i<=worker.length-1;i++){
			if(worker[i][1]>=mon){
				System.out.printf("%3d",worker[i][0]);
			}
		}
		System.out.printf("  共%d人",sum);
	}

}
