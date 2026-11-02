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
