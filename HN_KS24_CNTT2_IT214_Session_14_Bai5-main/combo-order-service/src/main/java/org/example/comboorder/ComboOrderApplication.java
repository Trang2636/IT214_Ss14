package org.example.comboorder;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;

@EnableFeignClients
@SpringBootApplication
public class ComboOrderApplication {
    public static void main(String[] args) {
        SpringApplication.run(ComboOrderApplication.class, args);
    }
}

