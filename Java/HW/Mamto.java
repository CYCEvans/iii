package com.xxx.HW;

public class Mamto implements Runnable{
	@Override
	public void run(){
		for(int i = 1;i<=10;i++){
			try {
				System.out.printf("饅頭人吃第%d碗飯%n",i);
				Thread.sleep(500+((int) (Math.random()*2501)));
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			
		}
		System.out.println("饅頭人吃完惹~~");
	}
}
