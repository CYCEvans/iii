package com.xxx.HW;

import java.util.ArrayList;

public class HW05_2 {

	public static void main(String[] args) {
		genAuthCode();
	}
//	回傳一個8位數的驗證碼
	static void genAuthCode(){
		//先建立48-57、65-90、97-122的ArrayLists(10進位代碼)
		ArrayList <Integer> arr = new ArrayList<> ();
		ArrayList <Integer> newAr = new ArrayList<> ();
		for(int i=48;i<123;i++){
			if((i<58) || ((i>64))&&(i<91)||(i>96)){
				arr.add(i);
			}
		}
//		for(int x : arr){
//			System.out.print((char)x);
//		}
//		System.out.println(arr.size());
		for(int i=0;i<8;i++){
			int index = (int)(Math.random()*arr.size());
			int number = arr.get(index);
			newAr.add(number);
			arr.remove(index);
			}
		for(int x : newAr){
			System.out.print((char)x);
		}
	}
}
