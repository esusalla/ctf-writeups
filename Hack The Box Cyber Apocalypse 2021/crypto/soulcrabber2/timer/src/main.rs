use std::time::SystemTime;
fn main() {
    let seed = SystemTime::now()
            .duration_since(SystemTime::UNIX_EPOCH)
            .expect("Time is broken")
            .as_secs();
    println!("{}", seed);
}
