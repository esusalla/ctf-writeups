use std::env;
use rand::{Rng,SeedableRng};
use rand::rngs::StdRng;

fn main() -> std::io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let seed = args[1].parse::<u64>().unwrap();
    let mut rng = StdRng::seed_from_u64(seed);
    for _ in 1..42 {
        let num = rng.gen::<u8>();
        print!("{} ", num); 
    }
    Ok(())
}
