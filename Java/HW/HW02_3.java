package com.xxx.HW;
import java.util.Arrays;
//阿文很喜歡簽大樂透(1～49)，但他是個善變的人，上次討厭數字是4，但這次他想要依心情決定討厭哪個數字，請您設計一隻程式，
//讓阿文可以輸入他不想要的數字，畫面會顯示他可以選擇的號碼與總數：
//*在這些號碼中選六個不重複
import java.util.Scanner;
public class HW02_3 {		
	public static void main(String[] args) {
		int sum =0;
		Scanner sc= new Scanner(System.in);
		System.out.println("請輸入不想要的數字");
		int num = sc.nextInt();
		
		for (int n =1;n<=49;n++){
			if(n/10 != num && n%10 !=num){
				sum +=1;
				System.out.printf("%2d%2c", n , sum% 6 == 0 ? '\n' : ' ');
//				if (sum%6 ==0){
//					System.out.printf("%3d%n",n);}
//				else{
//					System.out.printf("%3d",n);
//				}
			}
		}
		System.out.println();
		System.out.printf("總共有%d個%n",sum);
		int [] screen = new int[sum];
		int i = 0;
		for(int n =1;n<=49;n++){
			if(n/10 != num && n%10 !=num){
				screen[i]=n;
				i +=1;}
			}
		int[] lote= new int[6];
		Arrays.fill(lote, 50); // 6個50元素的陣列
		int count = 0;
		while (count <= 5){
			int random =(int) (Math.random()*sum); //0~sum-1的亂數取一
			Arrays.sort(lote);// 每次都要整理數列才能比較
			if (Arrays.binarySearch( lote, screen[random]) <0){ // 比較原來陣列和取出的亂數index值來比較小於0(不相同值)，插入其值
				lote[count] = screen[random];
				count +=1; 
			}
			else{continue;}
		}
		for(int number: lote){
			System.out.printf("%d%n", number);
		}
	}

}
