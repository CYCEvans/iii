package com.xxx.HW;

import java.io.*;

public class Cat  implements Serializable,Animals{

	private static final long serialVersionUID = 2857156072417228367L;
	private String name;
	
	public Cat(String name) {
		this.name = name;
	}
	@Override
	
	public void speak() {
		System.out.println("This is Cat " + name + " speaking!");
	}
	
}
