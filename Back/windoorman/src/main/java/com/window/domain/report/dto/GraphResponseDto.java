package com.window.domain.report.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.elasticsearch.annotations.Field;
import org.springframework.data.elasticsearch.annotations.FieldType;

import java.time.LocalDateTime;

@Getter
@NoArgsConstructor
public class GraphResponseDto {

    @Builder
    public GraphResponseDto(Double pm10, Double pm25, Double humid, Long co2, Long tvoc, LocalDateTime timestamp) {
        this.pm10 = pm10;
        this.pm25 = pm25;
        this.humid = humid;
        this.co2 = co2;
        this.tvoc = tvoc;
        this.timestamp = timestamp;
    }


    private Double pm10;
    private Double pm25;
    private Double humid;
    private Long co2;
    private Long tvoc;

    @Field(name = "@timestamp", type = FieldType.Date)
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime timestamp;
}
