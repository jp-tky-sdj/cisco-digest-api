from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import html

app = FastAPI(
    title="Cisco Digest Renderer API",
    description="Outlook MSO 準拠 HTML メールを決定論的に合成する API",
    version="1.0.0"
)

# セキュリティ用の簡易 API キー（お好きな英数字に変更可能）
API_KEY = "cisco-secret-key-2026"

class DigestItem(BaseModel):
    topic_name: str
    title: str
    raw_web_url: Optional[str] = ""
    source_type: Optional[str] = "SharePoint"
    location_path: Optional[str] = "-"
    updated_at: Optional[str] = "-"
    author: Optional[str] = "-"
    verbatim_quote: Optional[str] = ""
    summary: Optional[str] = ""

class RenderRequest(BaseModel):
    day_of_week: str
    target_topics: str
    items: List[DigestItem]

class RenderResponse(BaseModel):
    html_content: str

@app.post("/render", response_model=RenderResponse, summary="HTML メールを合成する")
def render_email(payload: RenderRequest, x_api_key: Optional[str] = Header(None)):
    # 簡易 API キー認証
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    cards_html = []
    for idx, item in enumerate(payload.items, 1):
        topic = html.escape(item.topic_name)
        title = html.escape(item.title)
        url = item.raw_web_url or ""
        source = html.escape(item.source_type or "SharePoint")
        location = html.escape(item.location_path or "-")
        updated = html.escape(item.updated_at or "-")
        author = html.escape(item.author or "-")
        quote = html.escape(item.verbatim_quote or "")
        summary = html.escape(item.summary or "")

        if url:
            title_part = f'<a href="{url}" target="_blank" style="color: #0284c7; text-decoration: underline; font-weight: 700; font-size: 13.5px;">{title}</a>'
        else:
            title_part = f'<span style="color: #475569; font-weight: 700; font-size: 13.5px;">{title}</span>'

        card = f'''
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="width: 100%; border: 1px solid #cbd5e1; border-radius: 6px; margin-bottom: 16px; background-color: #ffffff; overflow: hidden;">
<tbody>
  <tr>
    <td style="background-color: #f1f5f9; padding: 10px 16px; border-bottom: 1px solid #cbd5e1;">
      <div style="margin-bottom: 4px;">
        <span style="display: inline-block; background-color: #0f2d59; color: #ffffff; font-size: 11px; font-weight: 700; padding: 2px 7px; border-radius: 4px; margin-right: 6px;">#{idx} {topic}</span>
        {title_part}
      </div>
      <div style="font-size: 11px; color: #64748b; margin-top: 4px; line-height: 1.4;">
        <strong style="color: #334155;">ソース:</strong> {source} ｜ <strong style="color: #334155;">場所:</strong> {location} ｜ <strong style="color: #334155;">更新:</strong> {updated} ｜ <strong style="color: #334155;">作成者:</strong> {author}
      </div>
    </td>
  </tr>
  <tr>
    <td style="padding: 12px 16px;">
      <div style="margin-bottom: 10px;">
        <div style="font-weight: 700; font-size: 11px; color: #0369a1; text-transform: uppercase; margin-bottom: 3px;">【一次情報・完全一致原文抜粋】</div>
        <div style="background-color: #f8fafc; border-left: 3px solid #0284c7; padding: 8px 12px; font-family: Consolas, Monaco, monospace; font-size: 11.5px; color: #1e293b; line-height: 1.5; white-space: pre-wrap; word-break: break-all;">
{quote}
        </div>
      </div>
      <div>
        <div style="font-weight: 700; font-size: 11px; color: #15803d; text-transform: uppercase; margin-bottom: 3px;">【技術要点 ＆ SEアクション】</div>
        <div style="background-color: #f0fdf4; border-left: 3px solid #16a34a; padding: 8px 12px; font-size: 12px; color: #14532d; line-height: 1.5;">
{summary}
        </div>
      </div>
    </td>
  </tr>
</tbody>
</table>'''
        cards_html.append(card)

    joined_cards = "\n".join(cards_html)
    full_html = f'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cisco Security &amp; Technology Digest</title>
</head>
<body style="margin: 0; padding: 20px 0; background-color: #f8fafc; font-family: 'Segoe UI', Meiryo, Arial, sans-serif; color: #1e293b; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;">
<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="width: 100%; max-width: 820px; margin: 0 auto; border-collapse: collapse; background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; overflow: hidden;">
<tbody>
  <tr>
    <td style="background-color: #0f2d59; padding: 22px 28px; text-align: left; color: #ffffff; border-bottom: 3px solid #0284c7;">
      <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #38bdf8; margin-bottom: 4px;">
          Solutions Engineering Intelligence
      </div>
      <h2 style="margin: 0 0 6px 0; font-size: 20px; font-weight: 700; color: #ffffff; line-height: 1.3;">
        Cisco Security &amp; Technology Update Digest 【{html.escape(payload.day_of_week)}版】
      </h2>
      <div style="font-size: 12px; color: #cbd5e1; line-height: 1.4;">
        <strong style="color: #ffffff;">調査期間:</strong> 過去7日間 ｜ <strong style="color: #ffffff;">対象ソース:</strong> 全社SharePoint &amp; SalesConnect ｜ <strong style="color: #ffffff;">本日重点:</strong> {html.escape(payload.target_topics)}
      </div>
    </td>
  </tr>
  <tr>
    <td style="padding: 24px 28px;">
      <div style="font-size: 13.5px; margin-bottom: 20px; color: #334155; line-height: 1.6; border-left: 4px solid #0284c7; padding-left: 12px; background-color: #f0f9ff; padding-top: 8px; padding-bottom: 8px;">
        <strong>浅井様</strong><br>
        シスコ全社の情報資産（SharePoint / SalesConnect）より、直近1週間に新規追加・更新された対象領域の技術情報・一次資料の要約をご報告いたします。
      </div>

{joined_cards}

      <div style="margin-top: 28px; border-top: 1px solid #e2e8f0; padding-top: 14px; font-size: 11px; color: #64748b; line-height: 1.5; text-align: right;">
        Deterministic Pipeline Powered by MyAgent<br>
        East Public &amp; Geo Sector Solutions Engineering
      </div>
    </td>
  </tr>
</tbody>
</table>
</body>
</html>'''
    return RenderResponse(html_content=full_html)
