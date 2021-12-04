use std::env;

struct Random {
    seed: i32
}

impl Random {
    fn rand(&mut self) -> i32 {
        let a = 1103515245;
        let c = 12345;
        self.seed = self.seed.wrapping_mul(a) + c;
        (self.seed >> 16) & 0x7fff
    }
}

fn generate_password(rand: &mut Random, n: i32) -> String {
    (0..n).map(|_| (rand.rand() % (0x7f - 0x21) + 0x21) as u8 as char).collect::<String>()
}

fn main() -> std::io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let seed = args[1].parse::<i32>().unwrap();
    let mut rand = Random {
        seed
    };

    println!("{}", generate_password(&mut rand, 7));
    Ok(())
}
