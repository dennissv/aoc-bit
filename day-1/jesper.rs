use std::fs::File;
use std::io::{BufRead, BufReader};

//rust implementation of day 1 problem

fn main() {
	let fileReader = BufReader::new(File::open("data/input_jesper.txt").unwrap());
	let mut fuel = 0;
	let mut fuel_adjusted = 0;

	for line in fileReader.lines() {
		let str = line.unwrap();
		let module_cost=( (str.parse::<f32>().unwrap()/3.0).floor()-2.0) as i32;
		fuel+= module_cost;
		fuel_adjusted+= module_cost;
		let mut fuel_cost= ( (module_cost as f32/3.0).floor()-2.0) as i32;                

		while true {
			if( fuel_cost > 0){
				fuel_adjusted += fuel_cost;
				fuel_cost=( (fuel_cost as f32/3.0).floor()-2.0) as i32
			}else{
				break;
			}

		}

    	}
	//non-adjusted fuel cost
	print!("{}\n", fuel);
	//fuel cost adjusted for fuel weigth
	print!("{}\n", fuel_adjusted);

}

