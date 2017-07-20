package com.xxx.HW;

import java.util.*;

public class HW05_1 {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		System.out.println("請輸入N*M個四邊形星號");
		int m = sc.nextInt();
		int n = sc.nextInt();
		starSquare(n,m);
		System.out.println("--------------");
		randAvg();
		System.out.println("--------------");
		int [][] intArray = { {1,6,3},{9,5,2}};
		double [][] doubleArray = {{1.2,3.5,2.2},{7.4,2.1,8.2}};
		System.out.printf("intArray中最大為%d%n",maxElement(intArray));
		System.out.printf("doubleArray中最大為%f%n",maxElement(doubleArray));
		System.out.println("--------------");
		MyRectangle a = new MyRectangle();
		a.setWidth(10);
		a.setDepth(20);
		MyRectangle b = new MyRectangle(10,20);
		System.out.printf("a的面積為 %f%n",a.getArea());
		System.out.printf("b的面積為 %f%n",b.getArea());	
	}
//	請設計一個方法為starSquare(int width, int height)，當使用者鍵盤輸入寬與高時，即會印出對應的*長方形
	static void starSquare(int width, int height){
		String [][] arr = new String[width][height];
		for (String[] row: arr){
			for (String elems: row){
				System.out.print("*");
			}
			System.out.println();
		}
	}
//	請設計一個方法為randAvg()，從10個 0～100(含100)的整數亂數中取平均值並印出這10個亂數與平均值
	static void randAvg(){
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
		int sum = 0;
		System.out.println("本次亂數結果: ");
		for (int elem:newArr ){
			System.out.print(elem+" ");
			sum += elem;
		}
		System.out.printf("%n平均為%d%n",sum/newArr.size());
	}
	static int maxElement(int[][]x){
		ArrayList <Integer> arr = new ArrayList<> ();
		for(int[] row: x){
			for(int elem: row){
				arr.add(elem);
			}
		}
		Collections.sort(arr);
		return arr.get(arr.size()-1);
	}
	static double maxElement(double[][]x){
		ArrayList <Double> arr = new ArrayList<> ();
		for(double[] row: x){
			for(double elem: row){
				arr.add(elem);
			}
		}
		Collections.sort(arr);
		return arr.get(arr.size()-1);
	}
}
class MyRectangle{
	private double width;
	private double depth;
	public MyRectangle(){ }
	public MyRectangle(double width, double depth) {
		this.width = width;
		this.depth = depth;
	}
	public void setWidth(double width) {
		this.width = width;
	}
	public void setDepth(double depth) {
		this.depth = depth;
	}
	public double getArea() {
		return (depth*width);
	}
}	