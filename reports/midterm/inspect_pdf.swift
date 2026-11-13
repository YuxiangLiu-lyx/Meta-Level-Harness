// Read-only PDF inspection with separate text and image outputs.
import Foundation
import PDFKit
import AppKit

guard CommandLine.arguments.count == 3 else {
    fatalError("Usage: swift inspect_pdf.swift input.pdf new-output-directory")
}
let input = URL(fileURLWithPath: CommandLine.arguments[1])
let output = URL(fileURLWithPath: CommandLine.arguments[2], isDirectory: true)
guard !FileManager.default.fileExists(atPath: output.path) else {
    fatalError("Refusing to overwrite an existing inspection directory")
}
try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
guard let document = PDFDocument(url: input) else { fatalError("Cannot open PDF") }
var pages: [[String: Any]] = []
for i in 0..<document.pageCount {
    guard let page = document.page(at: i) else { fatalError("Missing page") }
    let bounds = page.bounds(for: .mediaBox)
    let text = page.string ?? ""
    let stem = String(format: "page-%02d", i + 1)
    try text.write(to: output.appendingPathComponent(stem + ".txt"), atomically: true, encoding: .utf8)
    let thumbnail = page.thumbnail(of: NSSize(width: bounds.width * 2, height: bounds.height * 2), for: .mediaBox)
    guard let tiff = thumbnail.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: tiff),
          let png = bitmap.representation(using: .png, properties: [:]) else {
        fatalError("Cannot render page")
    }
    try png.write(to: output.appendingPathComponent(stem + ".png"))
    var outside = 0
    for j in 0..<page.numberOfCharacters {
        let rectangle = page.characterBounds(at: j)
        if !rectangle.isEmpty && !bounds.insetBy(dx: -1, dy: -1).contains(rectangle) { outside += 1 }
    }
    pages.append([
        "page": i + 1, "width_pt": bounds.width, "height_pt": bounds.height,
        "characters": page.numberOfCharacters, "glyphs_outside_media_box": outside,
        "text_file": stem + ".txt", "render_file": stem + ".png",
        "links": page.annotations.compactMap { $0.url?.absoluteString }
    ])
}
var metadata: [String: String] = [:]
for (key, value) in document.documentAttributes ?? [:] { metadata[String(describing: key)] = String(describing: value) }
let report: [String: Any] = ["page_count": document.pageCount, "metadata": metadata, "pages": pages]
let json = try JSONSerialization.data(withJSONObject: report, options: [.prettyPrinted, .sortedKeys, .withoutEscapingSlashes])
try json.write(to: output.appendingPathComponent("inspection.json"))
print("Rendered and inspected \(document.pageCount) pages.")
