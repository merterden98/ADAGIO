mod utils;
use std::fs::File;
use std::io::prelude::*;
use pyo3::prelude::*; // Python importing
use clap::Clap; // Command line handling
use clap::{Arg, App};

// extern crate clap;

fn main() -> Result<T, E> {

    /* Use a clap package to handle command line parsing and put into a struct */

    let matches = App::new("TMap Program")
        .author("Kyla Levin, kateri.lalicker@tufts.edu")
        .version("1.0")
        .about("TMap Program")
        .arg(Arg::new("config")
            .short('c')
            .long("config")
            .value_name("FILE")
            .takes_value(true))
        .arg(Arg::new("INPUT")
            .required(true)
            .index(1))
        .arg(Arg::new("v")
            .short('v'))
        .get_matches();

    let mut file = File::create("output.txt").unwrap(); // Create output file with desired name
    file.write_all(b"Hello, world!"); // Write results to output file

    // Python::with_gil(|py| {
    //     let rarbanzo_r = PyModule::import(py, "Garbanzo").unwrap();
    //     let rwr_r = PyModule::import(py, "RandomWalkWithRestart").unwrap();

    //     // Testing purposes
    //     let test_feta_r = PyModule::import(py, "test_feta").unwrap();
    //     let x = test_feta_r.getattr("test_rwr").unwrap().call0().unwrap();
    //     Ok(())
    // });

    Ok(());
}
