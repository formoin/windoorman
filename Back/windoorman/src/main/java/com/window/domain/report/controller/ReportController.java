package com.window.domain.report.controller;

import com.window.domain.report.dto.ActionsReportResponseDto;
import com.window.domain.report.dto.AirReportDto;
import com.window.domain.report.dto.ReportResponseDto;
import com.window.domain.report.service.ReportService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/reports")
@RequiredArgsConstructor
@Slf4j
public class ReportController {

    private final ReportService reportService;

    @GetMapping("/{placeId}/{reportDate}")
    public ResponseEntity<?> findAirReport(@PathVariable Long placeId, @PathVariable LocalDate reportDate, Authentication authentication) {
        ReportResponseDto response = reportService.findAirReport(placeId, reportDate, authentication);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/actions/{windowId}/{reportDate}")
    public ResponseEntity<?> findActionReport(@PathVariable Long windowId,@PathVariable LocalDate reportDate, Authentication authentication) {
        List<ActionsReportResponseDto> responses = reportService.findActionsReport(windowId, reportDate, authentication);
        return ResponseEntity.ok(responses);
    }
}
