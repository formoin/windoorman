package com.window.domain.windows.dto.request;

import lombok.Getter;

@Getter
public class WindowsToggleRequestDto {
    private Long windowId;
    private Boolean isAuto;
}
