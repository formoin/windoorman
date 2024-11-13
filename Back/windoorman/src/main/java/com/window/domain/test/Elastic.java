package com.window.domain.test;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.persistence.Id;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Field;
import org.springframework.data.elasticsearch.annotations.FieldType;

import java.time.LocalDateTime;

@Getter
@Document(indexName = "#{T(java.time.LocalDate).now().toString()}", createIndex = false)
@AllArgsConstructor
public class Elastic {

    @Id
    private String id;

    @Field(name = "windowId", type = FieldType.Long)
    private Long windowsId;
    private Long memberId;

    private Double pm10;
    private Double pm25;
    private Double humid;
    private Long co2;
    private Long tvoc;

    @Field(name = "@timestamp", type = FieldType.Date)
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime timestamp;
}
