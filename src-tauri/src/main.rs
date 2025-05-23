#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use std::env;
use tauri::Manager;

fn main() {
    // Check if we're running in a Docker container (headless mode)
    let is_docker = env::var("IN_DOCKER").unwrap_or_else(|_| "false".to_string()) == "true";

    if is_docker {
        println!("Running in Docker container - headless mode activated");
        println!("Using frontend service at http://frontend:80");
        // In Docker, we don't attempt to show a window
        // Instead, we just keep the app running to show logs
        loop {
            std::thread::sleep(std::time::Duration::from_secs(60));
            println!("Tauri app is running in headless mode...");
        }
    } else {
        // Normal desktop mode
        tauri::Builder::default()
            .setup(|app| {
                #[cfg(debug_assertions)]
                {
                    let window = app.get_window("main").unwrap();
                    window.open_devtools();
                }
                Ok(())
            })
            .run(tauri::generate_context!())
            .expect("error while running tauri application");
    }
}
