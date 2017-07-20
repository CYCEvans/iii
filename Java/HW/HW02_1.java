package com.xxx.HW;
//請設計一隻程式，使用者輸入三個數字後，輸出結果會為正三角形、等腰三角形、直角三角形、其它三角形或不是三角形
import java.util.Scanner;
public class HW02_1 {
	public static void  checkTri(double a,double b,double c) {
		if ((a+b-c)>0||(a+c-b)>0||(b+c-a)>0 ){//是三角形
			if (a==b && b==c && c==a){
				System.out.println("是正三角形 ");//是正三角形 
			}
			else if ( a==b || b==c || c==a){
				System.out.println("是等腰三角形 ");//等腰三角
			}
			else if((a*a+b*b-c*c)*((a*a+c*c-b*b)*(b*b+c*c-a*a)) == 0){
				System.out.println("是值角三角形 ");//直角三角形(a^2+b^2-c^2)(a^2+c^2-b^2)(b^2+c^2-a^2) = 0
			}
			else if((a*a+b*b-c*c)*((a*a+c*c-b*b)*(b*b+c*c-a*a)) > 0){
				System.out.println("是銳角三角形 ");//銳角三角形(a^2+b^2-c^2)(a^2+c^2-b^2)(b^2+c^2-a^2) > 0
			}
			else if ((a*a+b*b-c*c)*((a*a+c*c-b*b)*(b*b+c*c-a*a)) < 0){
				System.out.println("是鈍角三角形 ");//鈍角三角形(a^2+b^2-c^2)(a^2+c^2-b^2)(b^2+c^2-a^2) > 0	
			}
		}
		else { System.out.println("不是三角形 ");}
		}
	public static void main(String[] args) {
		HW02_1 xta= new HW02_1();
		double a, b, c;
		Scanner sc =  new Scanner(System.in);
		System.out.println("輸入邊長a");
		a = sc.nextDouble();
		System.out.println("輸入邊長b");
		b = sc.nextDouble();
		System.out.println("輸入邊長c");
		c = sc.nextDouble();
		xta.checkTri(a,b,c);
	}

}
