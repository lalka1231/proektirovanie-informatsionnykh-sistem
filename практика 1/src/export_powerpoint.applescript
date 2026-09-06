set projectPath to "/Users/daniilvazdaev/Практическая_1_Проектирование_ИС/"
set deckPath to projectPath & "Практическая_работа_1_Проектирование_ИС.pptx"
set pdfPath to projectPath & "Практическая_работа_1_Проектирование_ИС.pdf"
tell application "Microsoft PowerPoint"
    open POSIX file deckPath
    set deck to active presentation
    save deck in pdfPath as save as PDF
end tell
