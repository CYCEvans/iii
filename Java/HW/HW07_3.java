package com.xxx.HW;

import java.io.*;

public class HW07_3 {

	public static void main(String[] args) throws IOException, ClassNotFoundException{
		File inputFile = new File("C:\\javawork\\www2.txt");
		File outputFile = new File("C:\\javawork\\www3.txt");
		File zoo = new File("C:\\data");
		zoo.mkdir();
		File myZoo = new File("C:\\data\\Object.dat");
//		copyFile(inputFile,outputFile);
		Animals[] zoomer = {new Cat("Laisy"),new Cat("Timmy"),new Dog("Lucky"),new Dog("Labooo")}; 
		copyObject(zoomer,myZoo);
		readObject(myZoo);
		
	
	}
//	請設計一個方法名為copyFile，這個方法有兩個參數。呼叫此方法時，第一個參數所代表的檔案會複製到第二個參數代表的檔案
	static void copyFile(File inputFile,File outputFile) throws IOException{
		try (FileReader in = new FileReader(inputFile);
		FileWriter out = new FileWriter(outputFile);){
			int num;
			while((num = in.read()) != -1){
					out.write(num);	
			}
		}
	}
	//Dog與Cat類別分別產生兩個物件，寫到C:\data\Object.dat裡
	static void copyObject(Animals[] anis, File file) throws IOException{
		try(FileOutputStream fr = new FileOutputStream(file); ){
			ObjectOutputStream oup = new ObjectOutputStream(fr);
			for(Animals ani:anis){
				oup.writeObject(ani);
			}
		}
	}
	
	static void readObject(File file) throws IOException, ClassNotFoundException{
		try(FileInputStream fr = new FileInputStream(file); ){
			ObjectInputStream inp = new ObjectInputStream(fr);
			while(true){
				((Animals) inp.readObject()).speak();
				System.out.println("--------------------");
			}
		}catch (EOFException e) {
			System.out.println("資料讀取完畢！");
		}
	}
}
