package com.xxx.HW;

class Account{
	private int money = 0;
	public final static int COUNTNUM= 10;
	synchronized public void deposit(int coco){
		if(Bear.index <COUNTNUM){
			while(money>2000){
				System.out.println("媽媽看到餘額在2000以上，停止匯款");
				try{
					wait();
				}catch(InterruptedException e){
					e.printStackTrace();
				}
			}
		}
		money += coco;
		System.out.printf("媽媽存了%d，戶頭共有: %d%n",coco,money);
		notify();
		
	}
	synchronized public void withdraw(int coco){
		while(money<coco){
			System.out.println("熊大發現沒$$，停止領錢");
			try{
				wait();
			}catch(InterruptedException e){
				e.printStackTrace();
			}
		}
		money -= coco;
		System.out.printf("熊大領了%d，戶頭共有: %d%n",coco,money);
		if (money <= 1000) {
			System.out.println("熊大看到餘額在1000以下，要求盡速匯款");
			notify();
		}
		else if(Bear.index ==10){
			notify();
		}
	}
}
class Mom extends Thread{
	Account account;
	public Mom(Account account) {
		this.account = account;
	}
	@Override
	public void run(){
		for(int i=1;i<=Account.COUNTNUM;i++){
			account.deposit(2000);
		}
	}
}
class Bear extends Thread{
	Account account;
	static int index; 
	public Bear(Account account) {
		this.account = account;
	}
	@Override
	public void run(){
		for(int i=1;i<=Account.COUNTNUM;i++){
			index =i;
			account.withdraw(1000);
		}
	}
}
public class HW09_2 {

	public static void main(String[] args) throws InterruptedException {
		Account account = new Account();
		Mom mom = new Mom(account);
		Bear bear = new Bear(account);
		mom.start();
		bear.start();
	}
}
