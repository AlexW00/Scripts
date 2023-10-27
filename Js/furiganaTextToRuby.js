function convertToRoundBrackets(str) {
  return str.replace(/\[/g, '(').replace(/\]/g, ')');
}
function convertToRuby(text) {
  const regex = /([\u3000-\u303F\u4E00-\u9FFF]+)\s*?\(([^)]+)\)/g;
  return text.replace(regex, '<ruby>$1<rp>(</rp><rt>$2</rt><rp>)</rp></ruby>');
}
