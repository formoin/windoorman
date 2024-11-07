package com.window.global.exception;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor(access = AccessLevel.PROTECTED)
public enum CustomException {

    NOT_FOUND_MEMBER_EXCEPTION(400, "NotFoundUserException", "유저가 존재하지 않습니다."),
    NOT_FOUND_PLACE_EXCEPTION(400, "NotFoundPlaceException", "장소가 존재하지 않습니다."),
    NOT_FOUND_WINDOWS_EXCEPTION(400, "NotFoundWindowsException", "창문이 존재하지 않습니다."),
    NOT_FOUND_SCHEDULE_EXCEPTION(400, "NotFoundScheduleException", "스케줄이 존재하지 않습니다."),
    NOT_FOUND_SCHEDULEGROUP_EXCEPTION(400, "NotFoundScheduleGroupException", "스케줄 그룹이 존재하지 않습니다."),
    EXPIRED_JWT_EXCEPTION(401, "ExpiredJwtException", "토큰이 만료됐습니다."),
    NOT_VALID_JWT_EXCEPTION(401, "NotValidJwtException", "유효하지 않는 토큰입니다."),
    NOT_FOUND_REFRESH_EXCEPTION(400, "NotFoundRefreshException", "리프레시 토큰이 존재하지 않습니다."),
    FAIL_SEND_SENSORS_EXCEPTION(400, "FailSendSensorsException", "센서 데이터 전송에 실패했습니다."),
    FAIL_CONNECT_SSE_EXCEPTION(400, "FailConnectSSEException", "SSE 연결에 실패했습니다."),
    ACCESS_DENIED_EXCEPTION(403,"AccessDeniedException","권한이 없습니다");

    private Integer statusNum;
    private String errorCode;
    private String errorMessage;
}
