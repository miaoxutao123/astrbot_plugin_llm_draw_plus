# AI自主绘图插件 (AstrBot Plugin)

AI自主绘图插件是一个为 [AstrBot](https://astrbot.app) 提供的插件，利用硅基流动 API，让 LLM 帮助用户生成图像。该插件适合轻量用户，支持通过自然语言描述生成高质量的图像。

## 功能

- 使用自然语言描述生成图像。
- 自动选择最适合的模型：
  - `black-forest-labs/FLUX.1-schnell`：适用于高分辨率、细节丰富、解剖精确的图像。
  - `stabilityai/stable-diffusion-3-5-large`：适用于真实皮肤纹理和多样化艺术风格的图像。
- 支持自定义图像大小和种子值。

## 安装

通过插件市场安装


## 配置

在 插件配置界面中配置以下参数：

- `api_key`：硅基流动 API 的密钥。
- `image_size`：图像尺寸（默认值为 `1024x1024`）。


## 开发者信息

- 作者：喵喵
- 仓库：[GitHub](https://github.com/miaoxutao123/astrbot_plugin_llm_draw_plus)
- 当前版本：v0.0.2

## 许可证

本项目基于 [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.html) 开源。

## 支持

如需帮助，请提交issue或者直接在交流群1群或3群中联系喵喵。