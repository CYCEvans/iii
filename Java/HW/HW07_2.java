package com.xxx.HW;

import java.io.*;
import java.util.*;

public class HW07_2 {

	public static void main(String[] args) {
		writeRandom();
	}
//	請寫一隻程式，能夠亂數產生10個1～1000的整數，並寫入一個名為Data.txt的檔案裡 (請參考本章講義第23頁，使用append方式觀察效果)
	static void writeRandom(){
		File outputFile = new File("data.txt");
		ArrayList <Integer> arr = new ArrayList<> ();
		for (int i = 1; i<101;i++){
			arr.add(i);
		}
		ArrayList <Integer> newArr = new ArrayList<>(10);
		for (int i = 0; i<10;i++){
			int index = (int)(Math.random()*(arr.size()));
			int number = arr.get(index);
			newArr.add(number);
			arr.remove(index);
		}
		try(FileOutputStream fos = new FileOutputStream(outputFile,true);
				PrintStream ps = new PrintStream(fos);){
			for (int x:newArr){
				ps.printf("%d ",x);
			}
			ps.println();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
