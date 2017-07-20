package com.xxx.HW;

public class HW09_1 {

	public static void main(String[] args) {
		
		System.out.println("-----大胃王快食競賽開始-----");
		James james = new James();
		Mamto mamto = new Mamto();
		Thread t1 = new Thread(james);
		Thread t2 = new Thread(mamto);
		t1.start();
		t2.start();
		try {
			t1.join();
			t2.join();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		System.out.println("-----大胃王快食競賽結束-----");
	}

}
